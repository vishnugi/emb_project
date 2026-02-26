from pathlib import Path
from embedded_log_labs.analyze import analyze_file, verdict

def test_analyze_file_and_verdict(tmp_path: Path):
    log = tmp_path / "device.log"
    log.write_text(
        "\n".join([
            "2026-01-01T00:00:00.000Z [INFO] boot ok",
            "2026-01-01T00:00:00.001Z [ERROR] sensor read failed",
            "2026-01-01T00:00:00.002Z [ERROR] sensor read failed",
            "2026-01-01T00:00:00.003Z [WARN] temp high",
        ]) + "\n",
        encoding="utf-8",
    )
    summary = analyze_file(log)
    assert summary.info == 1
    assert summary.warn == 1
    assert summary.error == 2
    assert verdict(summary, error_threshold=1).startswith("FAIL")
    assert verdict(summary, error_threshold=2) == "PASS"
