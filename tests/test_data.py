# Check tarot card data integrity

from dataclasses import FrozenInstanceError

import pytest

from tarot_package.models import Card
from tarot_package.data import DECK
from tarot_package.cards_major import MAJOR
from tarot_package.cards_wands import WANDS
from tarot_package.cards_cups import CUPS
from tarot_package.cards_swords import SWORDS
from tarot_package.cards_pentacles import PENTACLES


SUITS = ("wands", "cups", "swords", "pentacles")

RANKS = (
    "Ace", "Two", "Three", "Four", "Five",
    "Six", "Seven", "Eight", "Nine", "Ten",
    "Page", "Knight", "Queen", "King",
)


# Provide a known card for model tests
@pytest.fixture
def sample_card():
    return next(
        card for card in DECK
        if card.name == "The Fool"
    )

# DECK should contain every card from the five groups
def test_deck_combines_all_groups():
    expected = MAJOR + WANDS + CUPS + SWORDS + PENTACLES

    assert DECK == expected
    assert len(DECK) == len(expected)
    assert len(DECK) >= 5

def test_all_cards_are_card_objects():
    assert DECK

    for card in DECK:
        assert isinstance(card, Card), (
            f"Invalid card object: {card!r}"
        )

def test_card_names_are_unique():
    names = [card.name for card in DECK]

    assert len(names) == len(set(names))

def test_card_names_are_valid():
    for card in DECK:
        assert isinstance(card.name, str)
        assert card.name.strip(), "Card name is empty"
        assert card.name == card.name.strip()

def test_arcana_and_suit_consistency():
    for card in DECK:
        assert card.arcana in {"major", "minor"}, card.name

        if card.arcana == "major":
            assert card.suit is None, card.name
        else:
            assert card.suit in SUITS, card.name


# Each minor suit must contain all 14 ranks (?)
@pytest.mark.parametrize(
    "suit,cards",
    [
        ("wands", WANDS),
        ("cups", CUPS),
        ("swords", SWORDS),
        ("pentacles", PENTACLES),
    ],
)
def test_minor_arcana_completeness(suit, cards):
    expected_names = {
        f"{rank} of {suit.capitalize()}"
        for rank in RANKS
    }

    actual_names = {card.name for card in cards}

    assert len(cards) == 14
    assert actual_names == expected_names

    for card in cards:
        assert card.arcana == "minor"
        assert card.suit == suit

# Existing major cards must follow the correct structure
def test_major_arcana_structure():
    assert len(MAJOR) <= 22

    for card in MAJOR:
        assert card.arcana == "major"
        assert card.suit is None

# Meanings must be non-empty strings
def test_card_meanings_are_valid():
    for card in DECK:
        assert isinstance(card.upright, str), card.name
        assert isinstance(card.reversed, str), card.name

        assert card.upright.strip(), (
            f"{card.name}: empty upright meaning"
        )
        assert card.reversed.strip(), (
            f"{card.name}: empty reversed meaning"
        )

# Keywords must be a non-empty tuple of strings
def test_card_keywords_are_valid():
    for card in DECK:
        assert isinstance(card.keywords, tuple), card.name
        assert len(card.keywords) > 0, card.name

        for keyword in card.keywords:
            assert isinstance(keyword, str), card.name
            assert keyword.strip(), (
                f"{card.name}: empty keyword"
            )

# Card fields cannot be reassigned
def test_card_is_immutable(sample_card):
    assert isinstance(sample_card, Card)

    with pytest.raises(FrozenInstanceError):
        sample_card.name = "Changed"

    assert sample_card.name == "The Fool"
