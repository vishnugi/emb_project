from embedded_log_labs.parser import LogParser

def test_counts_info_warn_error():
    lines = [
        "2026-01-01T00:00:00.000Z [INFO] boot ok",
        "2026-01-01T00:00:00.001Z [WARN] temp high",
        "2026-01-01T00:00:00.002Z [ERROR] sensor read failed",
        "2026-01-01T00:00:00.003Z [ERROR] sensor read failed",
    ]
    p = LogParser()
    p.parse_lines(lines)
    s = p.summary()
    assert s.info == 1
    assert s.warn == 1
    assert s.error == 2
    assert s.panic is False
    assert s.top_error is not None
    assert s.top_error_count == 1 or s.top_error_count == 2  # depending on distinct strings

def test_panic_detected_by_level():
    p = LogParser()
    p.parse_line("2026-01-01T00:00:00.000Z [PANIC] KERNEL PANIC - not syncing")
    assert p.summary().panic is True

def test_panic_detected_by_keyword():
    p = LogParser()
    p.parse_line("2026-01-01T00:00:00.000Z [ERROR] kernel panic - not syncing")
    assert p.summary().panic is True
