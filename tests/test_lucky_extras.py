# Tests for the lucky_extras function

from datetime import date

import pytest

from tarot_package import Card, draw_cards, lookup_card, lucky_extras

CATEGORIES = ["color", "number", "advice"]


def make_card(name, suit, keywords=("alpha", "beta")):
    arcana = "major" if suit is None else "minor"
    return Card(
        name=name,
        arcana=arcana,
        suit=suit,
        upright="upright meaning",
        reversed="reversed meaning",
        keywords=keywords,
    )


# The lucky color depends on the suit of the first card
@pytest.mark.parametrize(
    "suit,expected",
    [
        ("wands", "Lucky color: red"),
        ("cups", "Lucky color: blue"),
        ("swords", "Lucky color: yellow"),
        ("pentacles", "Lucky color: green"),
        (None, "Lucky color: purple"),
    ],
)
def test_color_follows_suit(suit, expected):
    drawn = [(make_card("Test Card", suit), "upright")]

    assert lucky_extras(drawn, "color") == expected


# Color and number only look at the first drawn card
def test_color_and_number_use_first_card():
    first = make_card("Two of Cups", "cups")
    last = make_card("Ace of Wands", "wands")
    drawn = [(first, "upright"), (last, "upright")]

    assert lucky_extras(drawn, "color") == "Lucky color: blue"
    assert lucky_extras(drawn, "number") == lucky_extras([(first, "upright")], "number")


# The lucky number is one of the numbers listed for that suit
@pytest.mark.parametrize(
    "suit,options",
    [
        ("wands", (3, 8, 9)),
        ("cups", (2, 4, 10)),
        ("swords", (1, 6, 10)),
        ("pentacles", (1, 4, 8)),
        (None, (2, 5, 7)),
    ],
)
def test_number_comes_from_suit_options(suit, options):
    drawn = [(make_card("Some Card Name", suit), "upright")]
    result = lucky_extras(drawn, "number")

    assert result.startswith("Lucky number: ")
    assert int(result.removeprefix("Lucky number: ")) in options


# The number is picked from the card name length, so a known card gives a known number
def test_number_for_known_card():
    drawn = [(make_card("Two of Cups", "cups"), "upright")]

    # len("Two of Cups") == 11, and 11 % 3 == 2, so the third option (10) is used
    assert lucky_extras(drawn, "number") == "Lucky number: 10"


# Advice uses the last card and its orientation
def test_advice_uses_last_card_and_keyword():
    first = make_card("First Card", "wands", keywords=("firstword",))
    last = make_card("Last Card", "cups", keywords=("lastword",))
    result = lucky_extras([(first, "upright"), (last, "upright")], "advice")

    assert "lastword" in result
    assert "firstword" not in result


# Upright and reversed cards give different advice templates
def test_advice_differs_by_orientation():
    card = make_card("Test Card", "swords", keywords=("courage",))
    upright = lucky_extras([(card, "upright")], "advice")
    reversed_ = lucky_extras([(card, "reversed")], "advice")

    assert upright != reversed_
    assert "courage" in upright
    assert "courage" in reversed_


# Advice should be a complete sentence with the keyword filled in
def test_advice_has_no_unfilled_placeholder():
    card = make_card("Test Card", "swords", keywords=("courage",))

    for orientation in ("upright", "reversed"):
        result = lucky_extras([(card, orientation)], "advice")

        assert "{kw}" not in result
        assert result.endswith(".")


# The same input always gives the same output
@pytest.mark.parametrize("category", CATEGORIES)
def test_result_is_deterministic(category):
    drawn = draw_cards("Tracy", date=date(2026, 11, 8))

    assert lucky_extras(drawn, category) == lucky_extras(drawn, category)


# Every category works on a real three-card draw and returns text
@pytest.mark.parametrize("category", CATEGORIES)
def test_works_on_real_draw(category):
    drawn = draw_cards("Emma", date=date(2026, 11, 8))
    result = lucky_extras(drawn, category)

    assert isinstance(result, str)
    assert result.strip()


# Every card in the deck must produce a result for every category
@pytest.mark.parametrize("category", CATEGORIES)
def test_every_card_works(category):
    from tarot_package.data import DECK

    for card in DECK:
        for orientation in ("upright", "reversed"):
            assert lucky_extras([(card, orientation)], category)


# A single drawn card is enough
def test_single_card_draw():
    drawn = [(lookup_card("The Fool"), "upright")]

    assert lucky_extras(drawn, "color") == "Lucky color: purple"


# An unknown category should raise ValueError
@pytest.mark.parametrize("category", ["luck", "", "COLOR", None, 5])
def test_invalid_category(category):
    drawn = [(make_card("Test Card", "cups"), "upright")]

    with pytest.raises(ValueError):
        lucky_extras(drawn, category)


# An empty draw should raise ValueError
@pytest.mark.parametrize("category", CATEGORIES)
def test_empty_draw(category):
    with pytest.raises(ValueError):
        lucky_extras([], category)