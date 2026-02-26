from __future__ import annotations
import datetime
from typing import Final

ISO_Z_SUFFIX: Final[str] = "Z"

def utc_now_iso_ms() -> str:
    """Return UTC timestamp ISO format with milliseconds and Z suffix."""
    dt = datetime.datetime.now(datetime.timezone.utc)
    return dt.isoformat(timespec="milliseconds").replace("+00:00", ISO_Z_SUFFIX)
