import re
import difflib
from typing import Dict, List, Any, Optional

class TokenAttributionsDict(dict):
    """
    Dictionary mapping unique words to attribution scores for backwards compatibility,
    while attaching a structured list of individual token occurrences preserving
    position, occurrence index, and distinct attribution values without key overwriting.
    """
    def __init__(self, mapping: Dict[str, float], token_attributions: Optional[List[Dict[str, Any]]] = None):
        super().__init__(mapping)
        self.token_attributions: List[Dict[str, Any]] = token_attributions or []

    def get_token_attributions(self) -> List[Dict[str, Any]]:
        return self.token_attributions


def extract_words_with_positions(text: str) -> List[Dict[str, Any]]:
    """
    Extracts word tokens with 1-based position and occurrence index.
    """
    if not text or not text.strip():
        return []
    
    # Split using word boundary regex while keeping natural order
    matches = list(re.finditer(r'\b\w+\b', text))
    results = []
    seen_counts = {}
    
    for idx, match in enumerate(matches):
        word = match.group()
        w_lower = word.lower()
        seen_counts[w_lower] = seen_counts.get(w_lower, 0) + 1
        results.append({
            "token": word,
            "position": idx + 1,
            "occurrence": seen_counts[w_lower],
            "char_start": match.start(),
            "char_end": match.end()
        })
    return results


def align_token_attributions(
    orig_text: str,
    pert_text: str,
    orig_exp: Any,
    pert_exp: Any
) -> List[Dict[str, Any]]:
    """
    Aligns original and perturbed token attributions preserving occurrence identity
    and positions using sequence alignment. Prevents cross-matching of repeated words.
    """
    # 1. Resolve original token records
    if hasattr(orig_exp, "token_attributions") and orig_exp.token_attributions:
        orig_records = orig_exp.token_attributions
    else:
        orig_words = extract_words_with_positions(orig_text)
        exp_dict = dict(orig_exp) if isinstance(orig_exp, dict) else {}
        orig_records = []
        for w_info in orig_words:
            w = w_info["token"]
            val = exp_dict.get(w, exp_dict.get(w.lower(), None))
            orig_records.append({
                "token": w,
                "position": w_info["position"],
                "occurrence": w_info["occurrence"],
                "attribution": val
            })

    # 2. Resolve perturbed token records
    if hasattr(pert_exp, "token_attributions") and pert_exp.token_attributions:
        pert_records = pert_exp.token_attributions
    else:
        pert_words = extract_words_with_positions(pert_text)
        exp_dict = dict(pert_exp) if isinstance(pert_exp, dict) else {}
        pert_records = []
        for w_info in pert_words:
            w = w_info["token"]
            val = exp_dict.get(w, exp_dict.get(w.lower(), None))
            pert_records.append({
                "token": w,
                "position": w_info["position"],
                "occurrence": w_info["occurrence"],
                "attribution": val
            })

    # Count total occurrences for each word to distinguish repeated words
    orig_total_counts = {}
    for r in orig_records:
        tok_l = r["token"].lower()
        orig_total_counts[tok_l] = orig_total_counts.get(tok_l, 0) + 1

    pert_total_counts = {}
    for r in pert_records:
        tok_l = r["token"].lower()
        pert_total_counts[tok_l] = pert_total_counts.get(tok_l, 0) + 1

    # Keep track of running occurrence counters
    orig_seen = {}
    pert_seen = {}

    orig_tokens = [r["token"].lower() for r in orig_records]
    pert_tokens = [r["token"].lower() for r in pert_records]

    matcher = difflib.SequenceMatcher(None, orig_tokens, pert_tokens)
    aligned_rows = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for o_idx, p_idx in zip(range(i1, i2), range(j1, j2)):
                o_rec = orig_records[o_idx]
                p_rec = pert_records[p_idx]
                tok_l = o_rec["token"].lower()
                orig_seen[tok_l] = orig_seen.get(tok_l, 0) + 1
                pert_seen[tok_l] = pert_seen.get(tok_l, 0) + 1
                
                o_val = o_rec.get("attribution")
                p_val = p_rec.get("attribution")
                delta = (p_val - o_val) if (o_val is not None and p_val is not None) else None
                pol_change = (
                    o_val is not None and p_val is not None and 
                    ((o_val >= 0 and p_val < 0) or (o_val < 0 and p_val >= 0))
                )
                
                tot_occ = max(orig_total_counts.get(tok_l, 1), pert_total_counts.get(tok_l, 1))
                aligned_rows.append({
                    "token": p_rec["token"],
                    "orig_token": o_rec["token"],
                    "pert_token": p_rec["token"],
                    "orig_pos": o_rec["position"],
                    "pert_pos": p_rec["position"],
                    "orig_occ": orig_seen[tok_l],
                    "pert_occ": pert_seen[tok_l],
                    "total_occ": tot_occ,
                    "orig_val": o_val,
                    "pert_val": p_val,
                    "delta": delta,
                    "polarity_changed": pol_change,
                    "status": "aligned",
                    "is_key_shift": False
                })
        elif tag == 'replace':
            max_len = max(i2 - i1, j2 - j1)
            for offset in range(max_len):
                o_idx = i1 + offset if i1 + offset < i2 else None
                p_idx = j1 + offset if j1 + offset < j2 else None
                if o_idx is not None:
                    o_rec = orig_records[o_idx]
                    tok_l = o_rec["token"].lower()
                    orig_seen[tok_l] = orig_seen.get(tok_l, 0) + 1
                    tot_occ = orig_total_counts.get(tok_l, 1)
                    aligned_rows.append({
                        "token": o_rec["token"],
                        "orig_token": o_rec["token"],
                        "pert_token": None,
                        "orig_pos": o_rec["position"],
                        "pert_pos": None,
                        "orig_occ": orig_seen[tok_l],
                        "pert_occ": None,
                        "total_occ": tot_occ,
                        "orig_val": o_rec.get("attribution"),
                        "pert_val": None,
                        "delta": None,
                        "polarity_changed": False,
                        "status": "removed",
                        "is_key_shift": False
                    })
                if p_idx is not None:
                    p_rec = pert_records[p_idx]
                    tok_l = p_rec["token"].lower()
                    pert_seen[tok_l] = pert_seen.get(tok_l, 0) + 1
                    tot_occ = pert_total_counts.get(tok_l, 1)
                    aligned_rows.append({
                        "token": p_rec["token"],
                        "orig_token": None,
                        "pert_token": p_rec["token"],
                        "orig_pos": None,
                        "pert_pos": p_rec["position"],
                        "orig_occ": None,
                        "pert_occ": pert_seen[tok_l],
                        "total_occ": tot_occ,
                        "orig_val": None,
                        "pert_val": p_rec.get("attribution"),
                        "delta": None,
                        "polarity_changed": False,
                        "status": "inserted",
                        "is_key_shift": False
                    })
        elif tag == 'insert':
            for p_idx in range(j1, j2):
                p_rec = pert_records[p_idx]
                tok_l = p_rec["token"].lower()
                pert_seen[tok_l] = pert_seen.get(tok_l, 0) + 1
                tot_occ = pert_total_counts.get(tok_l, 1)
                aligned_rows.append({
                    "token": p_rec["token"],
                    "orig_token": None,
                    "pert_token": p_rec["token"],
                    "orig_pos": None,
                    "pert_pos": p_rec["position"],
                    "orig_occ": None,
                    "pert_occ": pert_seen[tok_l],
                    "total_occ": tot_occ,
                    "orig_val": None,
                    "pert_val": p_rec.get("attribution"),
                    "delta": None,
                    "polarity_changed": False,
                    "status": "inserted",
                    "is_key_shift": False
                })
        elif tag == 'delete':
            for o_idx in range(i1, i2):
                o_rec = orig_records[o_idx]
                tok_l = o_rec["token"].lower()
                orig_seen[tok_l] = orig_seen.get(tok_l, 0) + 1
                tot_occ = orig_total_counts.get(tok_l, 1)
                aligned_rows.append({
                    "token": o_rec["token"],
                    "orig_token": o_rec["token"],
                    "pert_token": None,
                    "orig_pos": o_rec["position"],
                    "pert_pos": None,
                    "orig_occ": orig_seen[tok_l],
                    "pert_occ": None,
                    "total_occ": tot_occ,
                    "orig_val": o_rec.get("attribution"),
                    "pert_val": None,
                    "delta": None,
                    "polarity_changed": False,
                    "status": "removed",
                    "is_key_shift": False
                })

    # Identify and flag the key Misweighted token occurrence
    aligned_candidates = [
        r for r in aligned_rows 
        if r["status"] == "aligned" and r["orig_val"] is not None and r["pert_val"] is not None
    ]
    if aligned_candidates:
        pol_candidates = [r for r in aligned_candidates if r["polarity_changed"]]
        if pol_candidates:
            key_row = max(pol_candidates, key=lambda r: abs(r["delta"] or 0.0))
            key_row["is_key_shift"] = True
        else:
            key_row = max(aligned_candidates, key=lambda r: abs(r["delta"] or 0.0))
            key_row["is_key_shift"] = True

    return aligned_rows
