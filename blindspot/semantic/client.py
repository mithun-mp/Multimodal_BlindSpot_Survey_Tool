"""
Gemini Semantic Reference Annotator Client (BlindSpot).
Integrates the official Google GenAI Python SDK for structured semantic reference annotations.

CRITICAL INVARIANTS:
- Gemini is NOT a benchmark model.
- Gemini is ONLY an external semantic-reference annotator/verification service.
- Gemini MUST NOT predict failure categories (BLIND, SPURIOUS, MISWEIGHTED, UNDETERMINED).
- Gemini MUST NOT predict whether any sentiment classifier will fail.
- Gemini structured output is strictly validated locally against {POSITIVE, NEGATIVE, NEUTRAL}.
- Confidence returned by Gemini is strictly recorded as "Gemini self-reported confidence",
  NOT empirical model certainty, ground-truth probability, or accuracy.
- Secure API key management via GEMINI_API_KEY or GOOGLE_API_KEY (never logged, never stored).
"""
import os
import json
import time
import logging
from typing import Dict, List, Optional, Any, Tuple, Union

try:
    from google import genai
    from google.genai import types as genai_types
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False

from .types import (
    SemanticReferenceLabel,
    SemanticRelation,
    SemanticAnnotation,
    VerificationStatus,
    ReferenceProvider,
)

logger = logging.getLogger("blindspot.semantic")


class GeminiSemanticClient:
    """
    Communicates with the official Google Gemini API via google-genai SDK
    to produce structured semantic reference annotations.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        fallback_model_name: Optional[str] = None,
        timeout_seconds: int = 15,
        max_retries: int = 3,
    ):
        if api_key is not None:
            raw_key = api_key.strip()
        else:
            raw_key = (
                os.environ.get("GEMINI_API_KEY", "").strip()
                or os.environ.get("GOOGLE_API_KEY", "").strip()
            )
            if not raw_key:
                # Check local .env file in workspace root
                root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
                if os.path.exists(root_env):
                    try:
                        with open(root_env, "r", encoding="utf-8") as f:
                            for line in f:
                                clean_line = line.strip()
                                if clean_line and not clean_line.startswith("#") and "=" in clean_line:
                                    k, v = clean_line.split("=", 1)
                                    k = k.strip()
                                    v = v.strip().strip('"').strip("'")
                                    if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                                        raw_key = v
                                        break
                    except Exception:
                        pass
        self.api_key = raw_key
        env_model = os.environ.get("GEMINI_MODEL", "").strip() or os.environ.get("GEMINI_SEMANTIC_MODEL", "").strip()
        if not env_model:
            root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
            if os.path.exists(root_env):
                try:
                    with open(root_env, "r", encoding="utf-8") as f:
                        for line in f:
                            clean_line = line.strip()
                            if clean_line and not clean_line.startswith("#") and "=" in clean_line:
                                k, v = clean_line.split("=", 1)
                                if k.strip() in ("GEMINI_MODEL", "GEMINI_SEMANTIC_MODEL"):
                                    env_model = v.strip().strip('"').strip("'")
                                    break
                except Exception:
                    pass
        self.model_name = (
            model_name
            or env_model
            or "gemini-3.8-flash"
        )
        self.fallback_model_name = (
            fallback_model_name
            or os.environ.get("GEMINI_FALLBACK_MODEL", "").strip()
            or os.environ.get("GEMINI_SEMANTIC_FALLBACK_MODEL", "").strip()
            or "gemini-2.5-flash"
        )
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

        # Telemetry tracking (Phase 16)
        self.requests_count: int = 0
        self.sentences_annotated_count: int = 0
        self.api_failures_count: int = 0
        self.retries_count: int = 0
        self.last_request_time: Optional[float] = None
        self.last_error: Optional[str] = None

        self._genai_client = None
        if self.is_online and HAS_GOOGLE_GENAI:
            try:
                self._genai_client = genai.Client(api_key=self.api_key)
            except Exception as ex:
                logger.warning(f"[SEMANTIC] Failed to initialize Google GenAI SDK: {ex}")
                self._genai_client = None

    @property
    def is_online(self) -> bool:
        """True strictly if a non-empty API key is configured."""
        return bool(self.api_key and self.api_key.strip())

    @property
    def status_string(self) -> str:
        if not self.is_online:
            return "Disabled (No API Key)"
        if not HAS_GOOGLE_GENAI and self._genai_client is None:
            return f"Connected ({self.model_name}) via REST"
        return f"Connected ({self.model_name})"

    def _get_structured_schema(self) -> Dict[str, Any]:
        """Strict JSON schema enforcing canonical labels, relations, and ambiguity."""
        return {
            "type": "OBJECT",
            "properties": {
                "annotations": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "sentence_id": {"type": "STRING"},
                            "semantic_polarity": {
                                "type": "STRING",
                                "enum": ["POSITIVE", "NEGATIVE", "NEUTRAL"],
                            },
                            "confidence": {
                                "type": "NUMBER",
                                "description": "Gemini self-reported confidence score between 0.0 and 1.0."
                            },
                            "reason_short": {"type": "STRING"},
                            "ambiguity": {
                                "type": "STRING",
                                "enum": ["LOW", "MEDIUM", "HIGH"]
                            },
                            "semantic_relation_to_baseline": {
                                "type": "STRING",
                                "enum": [
                                    "PRESERVE_POLARITY",
                                    "REVERSE_POLARITY",
                                    "SHIFT_TO_NEUTRAL",
                                    "SHIFT_FROM_NEUTRAL",
                                    "CONTRAST_SHIFT",
                                    "MEANING_CHANGED",
                                    "UNCERTAIN",
                                ],
                            },
                        },
                        "required": [
                            "sentence_id",
                            "semantic_polarity",
                            "confidence",
                            "reason_short",
                            "ambiguity",
                        ],
                    },
                }
            },
            "required": ["annotations"],
        }

    def _build_batch_prompt(
        self,
        baseline_text: str,
        probes: List[Dict[str, str]],
    ) -> str:
        """
        Builds the prompt for Gemini semantic annotation per Phase 5 scientific specifications.
        """
        prompt_lines = [
            "You are annotating semantic reference data for a research experiment.",
            "",
            "CRITICAL SCIENTIFIC INSTRUCTIONS:",
            "1. Do not predict how any target sentiment classifier will behave.",
            "2. Do not infer whether a model will fail.",
            "3. Do not classify a model as BLIND, SPURIOUS, MISWEIGHTED, or UNDETERMINED.",
            "4. For a text, determine its semantic sentiment polarity: POSITIVE, NEGATIVE, or NEUTRAL.",
            "5. For a pair of texts (baseline vs probe), determine the semantic relation between the original and perturbed text:",
            "   - PRESERVE_POLARITY: Affective sentiment direction remains identical.",
            "   - REVERSE_POLARITY: Sentiment polarity truly inverts (e.g., POSITIVE -> NEGATIVE).",
            "   - SHIFT_TO_NEUTRAL: Polar sentiment becomes neutral/objective.",
            "   - SHIFT_FROM_NEUTRAL: Neutral/factual statement becomes clearly emotional/evaluative.",
            "   - CONTRAST_SHIFT: Adversative clause or concession shifts primary emotional focus.",
            "   - MEANING_CHANGED: Semantic content changed without clean polarity inversion.",
            "   - UNCERTAIN: Context-dependent, idiomatic, or ambiguous effect.",
            "6. Distinguish linguistic/grammatical truth-condition changes from affective sentiment changes.",
            "   IMPORTANT: Do not assume that negation universally reverses sentiment polarity.",
            "   Example: 'The king is injured' (NEUTRAL/factual) -> 'The king is not injured' (NEUTRAL/absence of harm or POSITIVE relief, NOT NEGATIVE).",
            "7. If the semantic effect is ambiguous or context-dependent, return UNCERTAIN with ambiguity='HIGH'.",
            "8. You MUST include an annotation entry for the BASELINE text with sentence_id='baseline' (its semantic_relation_to_baseline can be PRESERVE_POLARITY), AND an annotation entry for each probe text with its respective ID.",
            "9. Return only the requested structured JSON matching the provided schema.",
            "",
            "SENTENCES TO ANNOTATE:",
            f"- ID: baseline | Type: baseline | Text: \"{baseline_text}\"",
        ]
        for p in probes:
            pid = p.get("probe_id", "")
            ptext = p.get("perturbed_text", "")
            ptype = p.get("perturbation_type", "")
            prompt_lines.append(f"- ID: {pid} | Type: {ptype} | Text: \"{ptext}\"")

        return "\n".join(prompt_lines)

    def annotate_batch(
        self,
        baseline_text: str,
        probes: List[Dict[str, str]],
    ) -> Dict[str, SemanticAnnotation]:
        """
        Annotates baseline and a list of probes in a single structured Gemini request.
        Returns a dict mapping sentence_id -> SemanticAnnotation.
        Uses official google-genai SDK if available, or direct REST fallback.
        """
        if not self.is_online:
            raise RuntimeError("Gemini API key is not configured. Client is in Offline / Manual mode.")

        prompt = self._build_batch_prompt(baseline_text, probes)
        schema = self._get_structured_schema()

        models_to_try = [self.model_name]
        if self.fallback_model_name and self.fallback_model_name != self.model_name:
            models_to_try.append(self.fallback_model_name)

        last_error = None
        for current_model in models_to_try:
            for attempt in range(self.max_retries):
                self.requests_count += 1
                self.last_request_time = time.time()
                try:
                    logger.info(f"[SEMANTIC] Calling Gemini API ({current_model}) attempt {attempt + 1}...")

                    # 1. Try google-genai SDK if available
                    if HAS_GOOGLE_GENAI and self._genai_client is not None:
                        try:
                            config = genai_types.GenerateContentConfig(
                                temperature=0.0,
                                response_mime_type="application/json",
                                response_schema=schema,
                            )
                            response = self._genai_client.models.generate_content(
                                model=current_model,
                                contents=prompt,
                                config=config,
                            )
                            text_response = response.text or ""
                            parsed = json.loads(text_response)
                            annotations_list = parsed.get("annotations", [])
                            result = self._validate_and_build_annotations(
                                annotations_list=annotations_list,
                                baseline_text=baseline_text,
                                probes=probes,
                                model_used=current_model,
                            )
                            self.sentences_annotated_count += len(result)
                            return result
                        except Exception as sdk_ex:
                            logger.warning(f"[SEMANTIC] google-genai SDK call failed: {sdk_ex}. Trying REST fallback...")

                    # 2. REST fallback with google generative language API
                    import requests
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{current_model}:generateContent?key={self.api_key}"
                    payload = {
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": 0.0,
                            "responseMimeType": "application/json",
                            "responseSchema": schema,
                        },
                    }
                    resp = requests.post(
                        url,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=self.timeout_seconds,
                    )

                    if resp.status_code == 200:
                        data = resp.json()
                        text_response = (
                            data.get("candidates", [{}])[0]
                            .get("content", {})
                            .get("parts", [{}])[0]
                            .get("text", "")
                        )
                        parsed = json.loads(text_response)
                        annotations_list = parsed.get("annotations", [])
                        result = self._validate_and_build_annotations(
                            annotations_list=annotations_list,
                            baseline_text=baseline_text,
                            probes=probes,
                            model_used=current_model,
                        )
                        self.sentences_annotated_count += len(result)
                        return result
                    elif resp.status_code in (429, 500, 503, 504):
                        self.retries_count += 1
                        time.sleep(1.0 * (attempt + 1))
                        continue
                    else:
                        self.api_failures_count += 1
                        last_error = f"Gemini API returned status {resp.status_code}: {resp.text[:300]}"
                        self.last_error = last_error
                        break

                except Exception as ex:
                    self.api_failures_count += 1
                    self.retries_count += 1
                    last_error = str(ex)
                    self.last_error = last_error
                    time.sleep(1.0 * (attempt + 1))

        raise RuntimeError(f"Gemini semantic annotation failed across models {models_to_try}: {last_error}")

    def parse_structured_response(self, text_response: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parses and strictly validates structured JSON from Gemini.
        Raises ValueError if non-canonical labels are encountered.
        """
        parsed = json.loads(text_response) if isinstance(text_response, str) else text_response
        if isinstance(parsed, dict) and "semantic_polarity" in parsed:
            label = parsed.get("semantic_polarity")
            if not SemanticReferenceLabel.is_valid(label):
                raise ValueError(f"Invalid semantic polarity: {label}")
            return parsed
        elif isinstance(parsed, dict) and "annotations" in parsed:
            for item in parsed["annotations"]:
                label = item.get("semantic_polarity")
                if not SemanticReferenceLabel.is_valid(label):
                    raise ValueError(f"Invalid semantic polarity in annotations: {label}")
            return parsed
        raise ValueError("Missing 'annotations' or 'semantic_polarity' in Gemini response.")

    def _parse_structured_response(self, text_response: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Backward-compatibility alias for parse_structured_response."""
        return self.parse_structured_response(text_response)

    def _validate_and_build_annotations(
        self,
        annotations_list: List[Dict[str, Any]],
        baseline_text: str,
        probes: List[Dict[str, str]],
        model_used: str,
    ) -> Dict[str, SemanticAnnotation]:
        """
        Strictly parses Gemini output into SemanticAnnotation objects.
        Confidence is recorded as Gemini self-reported confidence.
        """
        probe_texts = {p.get("probe_id", ""): p.get("perturbed_text", "") for p in probes}
        results: Dict[str, SemanticAnnotation] = {}

        for item in annotations_list:
            sid = str(item.get("sentence_id", "")).strip()
            raw_pol = item.get("semantic_polarity")

            # Strict validation
            if not SemanticReferenceLabel.is_valid(raw_pol):
                logger.warning(f"[SEMANTIC] Non-canonical polarity '{raw_pol}' for '{sid}'. Flagging.")
                continue

            pol = SemanticReferenceLabel.validate_label(raw_pol)
            raw_conf = item.get("confidence")
            conf = float(raw_conf) if raw_conf is not None else None
            # Clamp confidence between 0.0 and 1.0 if returned
            if conf is not None:
                conf = max(0.0, min(1.0, conf))

            reason = str(item.get("reason_short", item.get("reason", ""))).strip()
            ambiguity = str(item.get("ambiguity", "LOW")).upper()
            if ambiguity not in ("LOW", "MEDIUM", "HIGH"):
                ambiguity = "LOW"

            raw_rel = item.get("semantic_relation_to_baseline")
            rel = SemanticRelation.from_str(raw_rel) if raw_rel else None

            stext = baseline_text if sid == "baseline" else probe_texts.get(sid, "")

            annot = SemanticAnnotation(
                sentence_id=sid,
                sentence_text=stext,
                semantic_polarity=pol,
                confidence=conf,
                reason=reason,
                ambiguity=ambiguity,
                semantic_relation_to_baseline=rel,
                verification_status=VerificationStatus.AUTOMATED_REFERENCE,
                provider=ReferenceProvider.GEMINI.value,
                gemini_polarity=pol,
                gemini_confidence=conf,
                human_verified_polarity=None,
                final_semantic_polarity=pol,
                verification_source="GEMINI_AUTOMATED",
                model_used=model_used,
            )
            results[sid] = annot

        return results

    def get_usage_telemetry(self) -> Dict[str, Any]:
        """Returns full telemetry dictionary for monitoring and UI display."""
        return {
            "is_online": self.is_online,
            "status": self.status_string,
            "model_name": self.model_name,
            "requests_count": self.requests_count,
            "sentences_annotated_count": self.sentences_annotated_count,
            "api_failures_count": self.api_failures_count,
            "retries_count": self.retries_count,
            "last_request_time": self.last_request_time,
            "last_error": self.last_error,
        }
