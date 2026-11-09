"""Tests for the package's public API and the Card model."""
from dataclasses import fields

from tarot_package import Card, lookup_card


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