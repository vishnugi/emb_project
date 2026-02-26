from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Optional

from .simulator import device_log_stream

def capture_to_file(out_path: Path, *, lines: int, panic_prob: float, seed: Optional[int] = None) -> None:
    """Lab 2: capture generator output to a log file."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        for line in device_log_stream(lines, panic_prob=panic_prob, seed=seed):
            f.write(line + "\n")

def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Lab 2: Capture simulated device logs to a file.")
    p.add_argument("--out", required=True)
    p.add_argument("--lines", type=int, default=200)
    p.add_argument("--panic-prob", type=float, default=0.02)
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args(list(argv) if argv is not None else None)

    capture_to_file(Path(args.out), lines=args.lines, panic_prob=args.panic_prob, seed=args.seed)
    print(f"Wrote {args.lines} lines to {args.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
