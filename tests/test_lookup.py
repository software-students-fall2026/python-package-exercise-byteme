# Tests for the lookup_card function

import pytest

from tarot_package import Card, lookup_card
from tarot_package.data import DECK


# Exact card names should return the correct Card
@pytest.mark.parametrize(
    "query,expected",
    [
        ("The Fool", "The Fool"),
        ("The Magician", "The Magician"),
        ("Ace of Wands", "Ace of Wands"),
        ("Two of Cups", "Two of Cups"),
        ("Three of Swords", "Three of Swords"),
        ("Ace of Pentacles", "Ace of Pentacles"),
    ],
)
def test_lookup_exact_name(query, expected):
    result = lookup_card(query)

    assert isinstance(result, Card)
    assert result.name == expected

# Lookup should ignore case and surrounding whitespace
@pytest.mark.parametrize(
    "query,expected",
    [
        ("the fool", "The Fool"),
        ("THE MAGICIAN", "The Magician"),
        ("ace of wands", "Ace of Wands"),
        ("  Two of Cups  ", "Two of Cups"),
    ],
)
def test_lookup_case_and_whitespace(query, expected):
    assert lookup_card(query).name == expected

# Partial card names should be accepted
@pytest.mark.parametrize(
    "query,expected",
    [
        ("Magician", "The Magician"),
        ("Three of Pentacles", "Three of Pentacles"),
        ("Ace of Wands", "Ace of Wands"),
    ],
)
def test_lookup_partial_name(query, expected):
    assert lookup_card(query).name == expected

# Exact keyword matches should return the correct card
@pytest.mark.parametrize(
    "query,expected",
    [
        ("heartbreak", "Three of Swords"),
        ("new spark", "Ace of Wands"),
        ("resourcefulness", "The Magician"),
        ("self-reliance", "Nine of Pentacles"),
    ],
)
def test_lookup_keyword(query, expected):
    assert lookup_card(query).name == expected

# Minor spelling mistakes should be tolerated
def test_lookup_fuzzy_name():
    result = lookup_card("the magican")

    assert isinstance(result, Card)
    assert result.name == "The Magician"

# Empty or unmatched strings should raise ValueError
@pytest.mark.parametrize(
    "query",
    ["", " ", "\t\n", "zzzznotatarotcard"],
)
def test_lookup_invalid_value(query):
    with pytest.raises(ValueError):
        lookup_card(query)

@pytest.mark.parametrize(
    "query",
    [None, 42, [], {}],
)
def test_lookup_invalid_type(query):
    with pytest.raises(TypeError):
        lookup_card(query)

# Every card in DECK must be retrievable by its name
def test_lookup_all_cards():
    for card in DECK:
        result = lookup_card(card.name)

        assert result is card, (
            f"Lookup returned wrong card: {card.name}"
        )

# Lookup should return the Card stored in DECK
def test_lookup_returns_original_object():
    result = lookup_card("The Fool")

    matching_card = next(
        card for card in DECK
        if card.name == "The Fool"
    )

    assert result is matching_card
