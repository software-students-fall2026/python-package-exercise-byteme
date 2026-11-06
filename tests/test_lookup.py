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


# Every card in DECK should be retrievable by its name
@pytest.mark.parametrize(
    "card",
    DECK,
    ids=lambda card: card.name,
)
def test_lookup_all_cards(card):
    result = lookup_card(card.name)

    assert isinstance(result, Card)
    assert result.name == card.name
    assert result is card


# Lookup should return the Card stored in DECK
def test_lookup_returns_original_object():
    result = lookup_card("The Fool")

    matching_card = next(
        card for card in DECK
        if card.name == "The Fool"
    )

    assert result is matching_card


# Every card should be found regardless of case
@pytest.mark.parametrize(
    "card",
    DECK,
    ids=lambda card: card.name,
)
def test_lookup_all_cards_case_insensitive(card):
    result = lookup_card(card.name.swapcase())

    assert result.name == card.name
    assert result is card


# Surrounding whitespace must not affect lookup
@pytest.mark.parametrize(
    "card",
    DECK,
    ids=lambda card: card.name,
)
def test_lookup_all_cards_whitespace(card):
    result = lookup_card(f"  {card.name}  ")

    assert result.name == card.name
    assert result is card


# Every keyword should resolve to a valid matching card
@pytest.mark.parametrize(
    "keyword",
    sorted({
        word.casefold()
        for card in DECK
        for word in card.keywords
    }),
)
def test_lookup_all_keywords(keyword):
    result = lookup_card(keyword)

    # Exact name match
    for card in DECK:
        if card.name.casefold() == keyword:
            assert result is card
            return

    # Partial name match
    for card in DECK:
        if keyword in card.name.casefold():
            assert result is card
            return

    # Keyword match
    for card in DECK:
        if keyword in {
            word.casefold() for word in card.keywords
        }:
            assert result is card
            return

    pytest.fail(f"No card matches keyword: {keyword}")

