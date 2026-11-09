# Tests for the interpret_card function
import pytest

from tarot_package import interpret_card, lookup_card
from tarot_package.data import DECK

TOPICS = ["love", "career", "study", "money", "general"]
TONES = ["funny", "mystic", "programmer"]
ORIENTATIONS = ["upright", "reversed"]

TOPIC_CONTEXTS = {
    "love": "your relationships",
    "career": "your work and career",
    "study": "your education and learning",
    "money": "your finances and wealth",
    "general": "your overall life and well-being"
}

TONE_PREFIXES = {
    "mystic": "The cards whisper:",
    "funny": "Your tarot plot twist:",
    "programmer": "Card output:",
}

@pytest.fixture
def card():
    return next(c for c in DECK if c.name == "The Fool")

def meaning_for(card, orientation):
    if orientation == "upright":
        return card.upright
    else:
        return card.reversed

# Result should be non-empty string
@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("tone", TONES)
@pytest.mark.parametrize("orientation", ORIENTATIONS)


def test_interpret_returns_string(card, topic, tone, orientation):

    interpretation = interpret_card(card, topic, tone, orientation)

    assert isinstance(interpretation, str)
    assert interpretation.strip()

# Uses the correct meaning based on orientation
@pytest.mark.parametrize("orientation", ORIENTATIONS)
def test_interpret_uses_right_meaning(card, orientation):

    interpretation = interpret_card(card, "general", "mystic", orientation)
    expected_meaning = meaning_for(card, orientation)
    assert expected_meaning in interpretation