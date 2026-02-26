from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable, Optional

from .parser import LogParser, LogSummary

def verdict(summary: LogSummary, *, error_threshold: int = 2) -> str:
    if summary.panic:
        return "FAIL - PANIC"
    if summary.error > error_threshold:
        return "FAIL - TOO_MANY_ERRORS"
    return "PASS"

def analyze_file(in_path: Path) -> LogSummary:
    parser = LogParser()
    with in_path.open("r", encoding="utf-8", errors="ignore") as f:
        parser.parse_lines(f)
    return parser.summary()

def write_csv(summary: LogSummary, out_csv: Path, verdict_str: str) -> None:
    """Lab 5: write CSV report."""
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["info", "warn", "error", "panic", "verdict", "top_error", "top_error_count"])
        w.writerow([
            summary.info,
            summary.warn,
            summary.error,
            int(summary.panic),
            verdict_str,
            summary.top_error or "",
            summary.top_error_count,
        ])

def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Labs 3–5: Parse logs, detect panic, and generate CSV report.")
    p.add_argument("--in", dest="in_file", required=True)
    p.add_argument("--csv", dest="csv_out", required=True)
    p.add_argument("--error-threshold", type=int, default=2)
    args = p.parse_args(list(argv) if argv is not None else None)

    summary = analyze_file(Path(args.in_file))
    v = verdict(summary, error_threshold=args.error_threshold)
    write_csv(summary, Path(args.csv_out), v)

    print("===== LOG SUMMARY =====")
    print(f"INFO : {summary.info}")
    print(f"WARN : {summary.warn}")
    print(f"ERROR: {summary.error}")
    print(f"PANIC: {summary.panic}")
    if summary.top_error:
        print(f"Top ERROR: {summary.top_error}  ({summary.top_error_count} times)")
    print(f"VERDICT: {v}")
    print(f"CSV: {args.csv_out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
