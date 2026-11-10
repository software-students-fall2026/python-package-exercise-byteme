"""Smoke tests for examples/example.py."""
import subprocess
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "example.py"


def run_example():
    return subprocess.run(
        [sys.executable, str(EXAMPLE)],
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_example_file_exists():
    assert EXAMPLE.is_file()


def test_example_runs_without_error():
    result = run_example()
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_example_demonstrates_every_function():
    out = run_example().stdout
    for title in (
        "draw_cards(allow_reversed=True)",
        "draw_cards(allow_reversed=False)",
        "lookup_card",
        "interpret_card",
        "interpret_spread",
        "lucky_extras",
        "daily_reading",
    ):
        assert title in out, title


def test_example_output_has_reading_content():
    out = run_example().stdout
    assert "Past:" in out
    assert "Present:" in out
    assert "Future:" in out
    assert "Summary:" in out
    assert "Lucky color:" in out
    assert "Lucky number:" in out


def test_example_lookup_results():
    out = run_example().stdout
    assert "The Fool" in out
    assert "The Magician" in out
    assert "The High Priestess" in out


def test_example_is_deterministic():
    assert run_example().stdout == run_example().stdout