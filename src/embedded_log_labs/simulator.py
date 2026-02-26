from __future__ import annotations

import argparse
import random
import sys
import time
from typing import Generator, Iterable, Optional

from .utils import utc_now_iso_ms

INFO_MESSAGES = [
    "boot: system init complete",
    "net: link up (1Gbps)",
    "fs: mounted /data",
    "sensor: ready",
    "watchdog: armed",
    "app: service started",
    "telemetry: heartbeat ok",
]

WARN_MESSAGES = [
    "temp: threshold nearing (78C)",
    "net: retransmits increasing",
    "fs: slow write detected",
    "sensor: jitter high",
    "power: voltage dip detected",
]

ERROR_MESSAGES = [
    "i2c: bus arbitration lost",
    "sensor: read failed",
    "net: packet drop burst",
    "mmc: crc error on read",
    "app: unhandled error code=E42",
]

PANIC_MESSAGES = [
    "KERNEL PANIC - not syncing: Fatal exception",
    "panic: stack overflow in irq handler",
    "fatal exception: NULL dereference",
]

def device_log_stream(
    lines: int,
    *,
    panic_prob: float = 0.0,
    seed: Optional[int] = None,
    sleep_ms: int = 0
) -> Generator[str, None, None]:
    """Lab 1: generator that yields simulated embedded logs."""
    rng = random.Random(seed)
    for _ in range(lines):
        ts = utc_now_iso_ms()
        if panic_prob > 0 and rng.random() < panic_prob:
            yield f"{ts} [PANIC] {rng.choice(PANIC_MESSAGES)}"
        else:
            roll = rng.random()
            if roll < 0.70:
                yield f"{ts} [INFO] {rng.choice(INFO_MESSAGES)}"
            elif roll < 0.90:
                yield f"{ts} [WARN] {rng.choice(WARN_MESSAGES)}"
            else:
                yield f"{ts} [ERROR] {rng.choice(ERROR_MESSAGES)}"
        if sleep_ms > 0:
            time.sleep(sleep_ms / 1000.0)

def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Lab 1: Simulate device logs using a Python generator.")
    p.add_argument("--lines", type=int, default=50)
    p.add_argument("--panic-prob", type=float, default=0.0)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--sleep-ms", type=int, default=0)
    args = p.parse_args(list(argv) if argv is not None else None)

    for line in device_log_stream(args.lines, panic_prob=args.panic_prob, seed=args.seed, sleep_ms=args.sleep_ms):
        sys.stdout.write(line + "\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
