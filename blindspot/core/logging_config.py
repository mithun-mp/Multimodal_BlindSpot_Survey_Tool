"""
Structured Logging Configuration for BlindSpot Research Workstation.
Provides subsystem tagging (BOOT, UI, MODEL, CACHE, RUNNER, etc.),
rotating file logging in logs/blindspot.log, and configurable debug mode.
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


# Canonical Subsystems
SUBSYSTEMS = [
    "BOOT",
    "UI",
    "MODEL",
    "CACHE",
    "RUNNER",
    "PROBE",
    "XAI",
    "RESOURCE",
    "STORAGE",
    "REPORT",
]


class SubsystemFormatter(logging.Formatter):
    """
    Formats log records into:
    YYYY-MM-DD HH:MM:SS | LEVEL    | SUBSYSTEM | Message
    """
    def format(self, record: logging.LogRecord) -> str:
        t_str = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        lvl = record.levelname.ljust(8)
        subsystem = getattr(record, "subsystem", "GENERAL").upper().ljust(9)
        msg = record.getMessage()
        return f"{t_str} | {lvl} | {subsystem} | {msg}"


def get_subsystem_logger(subsystem: str = "GENERAL", name: Optional[str] = None) -> logging.LoggerAdapter:
    """
    Returns a LoggerAdapter with subsystem metadata injected into log records.
    """
    base_logger = logging.getLogger(name or f"blindspot.{subsystem.lower()}")
    return logging.LoggerAdapter(base_logger, {"subsystem": subsystem})


def configure_workstation_logging(
    log_dir: str = "logs",
    log_file: str = "blindspot.log",
    max_bytes: int = 5 * 1024 * 1024,  # 5 MB per file
    backup_count: int = 5,
    debug_mode: bool = False,
) -> None:
    """
    Initializes rotating file logger and console handlers with structured subsystem formatting.
    """
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    root_logger = logging.getLogger("blindspot")
    root_level = logging.DEBUG if debug_mode else logging.INFO
    root_logger.setLevel(root_level)

    # Clear existing handlers to prevent duplicate lines
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = SubsystemFormatter()

    # Rotating File Handler
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(root_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Standard Console Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(root_level)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)


def close_workstation_logging() -> None:
    """Closes and removes all handlers from the blindspot logger."""
    root_logger = logging.getLogger("blindspot")
    for handler in list(root_logger.handlers):
        try:
            handler.close()
        except Exception:
            pass
        root_logger.removeHandler(handler)

