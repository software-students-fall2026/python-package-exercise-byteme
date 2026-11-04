"""Tests for functionality already implemented in the sample-card snapshot."""
from dataclasses import FrozenInstanceError, fields

import pytest

from tarot_package import Card, lookup_card
from tarot_package.data import DECK


def test_public_api():
    import tarot_package
    for name in tarot_package.__all__:
        assert hasattr(tarot_package, name), name


def test_card_model():
    card = lookup_card('The Fool')
    assert isinstance(card, Card)
    assert {f.name for f in fields(Card)} == {
        'name', 'arcana', 'suit', 'upright', 'reversed', 'keywords'
    }
    assert isinstance(card.keywords, tuple)
    with pytest.raises(FrozenInstanceError):
        card.name = 'Changed'


def test_sample_deck():
    names = {card.name for card in DECK}
    assert len(DECK) >= 5
    assert len(names) == len(DECK)
    assert {'The Fool', 'The Magician', 'Two of Cups',
            'Three of Swords', 'Ace of Pentacles'} <= names


@pytest.mark.parametrize('query,expected', [
    ('The Fool', 'The Fool'),
    ('the fool', 'The Fool'),
    ('  THE MAGICIAN  ', 'The Magician'),
    ('Magician', 'The Magician'),
    ('heartbreak', 'Three of Swords'),
    ('the magican', 'The Magician'),
])
def test_lookup_valid(query, expected):
    assert lookup_card(query).name == expected


@pytest.mark.parametrize('query', ['', ' ', '\t\n', 'zzzznotatarotcard'])
def test_lookup_invalid_value(query):
    with pytest.raises(ValueError):
        lookup_card(query)


@pytest.mark.parametrize('query', [None, 42, [], {}])
def test_lookup_invalid_type(query):
    with pytest.raises(TypeError):
        lookup_card(query)


def test_sample_card_fields():
    for card in DECK:
        assert card.arcana in {'major', 'minor'}
        assert card.suit in {None, 'wands', 'cups', 'swords', 'pentacles'}
        assert card.suit is None if card.arcana == 'major' else card.suit is not None
        assert card.upright.strip()
        assert card.reversed.strip()
        assert card.keywords
