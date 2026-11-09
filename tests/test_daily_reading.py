from datetime import date
from tarot_package import daily_reading, draw_cards, lucky_extras
import pytest

def test_daily_reading_rejects_invalid_topic():
    with pytest.raises(ValueError):
        daily_reading(
            "Uuree",
            date=date(2026, 11, 8),
            topic="invalid-topic",
            tone="mystic",
        )


def test_daily_reading_includes_matching_extras():
    day = date(2026, 11, 8)
    drawn = draw_cards("Uuree", date=day)

    result = daily_reading("Uuree", date=day)

    assert lucky_extras(drawn, "color") in result
    assert lucky_extras(drawn, "number") in result
    assert lucky_extras(drawn, "advice") in result

def test_daily_reading_is_deterministic():
    first = daily_reading(
        "Uuree",
        date=date(2026, 11, 8),
        topic="study",
        tone="programmer",
    )

    second = daily_reading(
        "Uuree",
        date=date(2026, 11, 8),
        topic="study",
        tone="programmer",
    )

    assert first == second


def test_daily_reading_contains_expected_sections():
    result = daily_reading(
        "Uuree",
        date=date(2026, 11, 8),
        topic="study",
        tone="programmer",
    )

    assert isinstance(result, str)
    assert "Reading for Uuree" in result
    assert "Past:" in result
    assert "Present:" in result
    assert "Future:" in result
    assert "Summary:" in result
    assert "Lucky color:" in result
    assert "Lucky number:" in result

def test_daily_reading_rejects_invalid_tone():
    with pytest.raises(ValueError):
        daily_reading(
            "Uuree",
            date=date(2026, 11, 8),
            topic="study",
            tone="invalid-tone",
        )

def test_daily_reading_rejects_blank_name():
    with pytest.raises(ValueError):
        daily_reading(
            "   ",
            date=date(2026, 11, 8),
        )

def test_daily_reading_rejects_string_date():
    with pytest.raises(TypeError):
        daily_reading(
            "Uuree",
            date="2026-11-08",
        )