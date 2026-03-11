from __future__ import annotations

from pathlib import Path
import os
import sys


def load_dotenv(path: str | Path | None = None) -> None:
    """Load simple KEY=VALUE pairs from a dotenv file into os.environ."""
    if path is not None:
        candidates = [Path(path)]
    else:
        candidates = [Path.cwd() / ".env"]
        if getattr(sys, "frozen", False):
            candidates.append(Path(sys.executable).resolve().parent / ".env")

    env_path = next((candidate for candidate in candidates if candidate.exists()), None)
    if env_path is None:
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_env_int(key: str, default: int) -> int:
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def get_env_bool(key: str, default: bool) -> bool:
    value = os.getenv(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}
