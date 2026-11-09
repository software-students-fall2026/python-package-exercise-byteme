# Tests for draw_cards

from datetime import date, datetime
import random

import pytest

from tarot_package import Card, draw_cards
from tarot_package.data import DECK


TEST_DATE = date(2026, 11, 9)


def test_default_draw():
    drawn = draw_cards("Alice", TEST_DATE)

    assert len(drawn) == 3
    assert all(isinstance(card, Card) for card, _ in drawn)
    assert all(
        orientation in ("upright", "reversed")
        for _, orientation in drawn
    )


def test_draw_is_deterministic():
    first = draw_cards("Alice", TEST_DATE)
    second = draw_cards("Alice", TEST_DATE)

    assert first == second


def test_draw_has_no_duplicates():
    drawn = draw_cards("Alice", TEST_DATE, count=78)
    cards = [card for card, _ in drawn]

    assert len(cards) == 78
    assert len(set(cards)) == 78
    assert set(cards) == set(DECK)


def test_draw_without_reversed():
    drawn = draw_cards(
        "Alice",
        TEST_DATE,
        count=20,
        allow_reversed=False,
    )

    assert len(drawn) == 20
    assert all(o == "upright" for _, o in drawn)


def test_name_whitespace():
    first = draw_cards("Alice", TEST_DATE)
    second = draw_cards("  Alice  ", TEST_DATE)

    assert first == second


@pytest.mark.parametrize("count", [1, 3, 78])
def test_valid_count(count):
    drawn = draw_cards("Alice", TEST_DATE, count=count)

    assert len(drawn) == count
    assert len({card for card, _ in drawn}) == count


@pytest.mark.parametrize("count", [0, -1, 79])
def test_invalid_count_value(count):
    with pytest.raises(ValueError):
        draw_cards("Alice", TEST_DATE, count=count)


@pytest.mark.parametrize("count", [1.5, "3", None, True])
def test_invalid_count_type(count):
    with pytest.raises(TypeError):
        draw_cards("Alice", TEST_DATE, count=count)


@pytest.mark.parametrize("name", ["", " ", "\t"])
def test_blank_name(name):
    with pytest.raises(ValueError):
        draw_cards(name, TEST_DATE)


@pytest.mark.parametrize("name", [None, 42, [], {}])
def test_invalid_name_type(name):
    with pytest.raises(TypeError):
        draw_cards(name, TEST_DATE)


@pytest.mark.parametrize("bad_date", [
    "2026-11-09",
    123,
    datetime(2026, 11, 9),
])
def test_invalid_date_type(bad_date):
    with pytest.raises(TypeError):
        draw_cards("Alice", bad_date)


@pytest.mark.parametrize("value", [None, 0, "False"])
def test_invalid_allow_reversed(value):
    with pytest.raises(TypeError):
        draw_cards(
            "Alice",
            TEST_DATE,
            allow_reversed=value,
        )


def test_global_random_state_unchanged():
    before = random.getstate()

    draw_cards("Alice", TEST_DATE)

    after = random.getstate()
    assert before == after
