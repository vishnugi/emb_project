from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, List, Optional

LEVEL_RE = re.compile(r"\[(INFO|WARN|ERROR|PANIC)\]")
PANIC_KEYWORDS_RE = re.compile(r"(kernel\s+panic|\bpanic:|fatal\s+exception)", re.IGNORECASE)

@dataclass(frozen=True)
class LogSummary:
    info: int
    warn: int
    error: int
    panic: bool
    top_error: Optional[str]
    top_error_count: int

class LogParser:
    """Lab 3 + 4: parse logs + detect panic."""

    def __init__(self) -> None:
        self.info_count = 0
        self.warn_count = 0
        self.error_lines: List[str] = []
        self.panic_detected = False

    def parse_line(self, line: str) -> None:
        if PANIC_KEYWORDS_RE.search(line):
            self.panic_detected = True

        m = LEVEL_RE.search(line)
        if not m:
            return

        level = m.group(1)
        if level == "INFO":
            self.info_count += 1
        elif level == "WARN":
            self.warn_count += 1
        elif level == "ERROR":
            self.error_lines.append(line.strip())
        elif level == "PANIC":
            self.panic_detected = True

    def parse_lines(self, lines: Iterable[str]) -> None:
        for ln in lines:
            self.parse_line(ln)

    def summary(self) -> LogSummary:
        c = Counter(self.error_lines)
        top_error, top_count = (None, 0)
        if c:
            top_error, top_count = c.most_common(1)[0]
        return LogSummary(
            info=self.info_count,
            warn=self.warn_count,
            error=len(self.error_lines),
            panic=self.panic_detected,
            top_error=top_error,
            top_error_count=top_count,
        )
