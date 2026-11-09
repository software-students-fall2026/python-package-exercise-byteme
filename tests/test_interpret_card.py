# Tests for the interpret_card function
import pytest

from tarot_package import interpret_card
from tarot_package.data import DECK

TOPICS = ["love", "career", "study", "money", "general"]
TONES = ["funny", "mystic", "programmer"]
ORIENTATIONS = ["upright", "reversed"]

TOPIC_CONTEXTS = {
    "love": "your relationships",
    "career": "your work and career",
    "study": "your learning and studies",
    "money": "your money and resources",
    "general": "your daily life",
}

TONE_PREFIXES = {
    "mystic": "The cards whisper:",
    "funny": "Your tarot plot twist:",
    "programmer": "Card output:",
}

EXPECTED_TEMPLATES = {
    "mystic": (
        "The cards whisper: {meaning} "
        "In {context}, let these themes guide your reflection: {keywords}."
    ),
    "funny": (
        "Your tarot plot twist: {meaning} "
        "For {context}, keep {keywords} on the guest list. Bring snacks."
    ),
    "programmer": (
        "Card output: {meaning} "
        "For {context}, debug your next step with these keywords: {keywords}."
    ),
}


@pytest.fixture
def card():
    return next(c for c in DECK if c.name == "The Fool")


def meaning_for(card, orientation):
    if orientation == "upright":
        return card.upright
    else:
        return card.reversed


# Results should be non-empty string
@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("tone", TONES)
@pytest.mark.parametrize("orientation", ORIENTATIONS)
def test_interpret_returns_string(card, orientation, topic, tone):
    interpretation = interpret_card(card, orientation, topic, tone)
    assert isinstance(interpretation, str)
    assert interpretation.strip()


# Uses the correct meaning based on orientation
@pytest.mark.parametrize("orientation", ORIENTATIONS)
@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("tone", TONES)
def test_interpret_uses_right_meaning(card, orientation, topic, tone):
    interpretation = interpret_card(card, orientation, topic, tone)
    expected_meaning = meaning_for(card, orientation)
    assert expected_meaning in interpretation


# Each topic should have their own context phrase
@pytest.mark.parametrize("topic", TOPICS)
def test_interpret_includes_topic_context(card, topic):
    interpretation = interpret_card(card, "upright", topic, "mystic")
    expected_context = TOPIC_CONTEXTS[topic]
    assert expected_context in interpretation


# Different orientations should give different outputs
def test_interpret_differs_by_orientation(card):
    upright = interpret_card(card, "upright", "general", "mystic")
    reverse = interpret_card(card, "reversed", "general", "mystic")
    assert upright != reverse


# Each tone should follow its own template
@pytest.mark.parametrize("tone", TONES)
def test_interpret_follows_tone_template(card, tone):
    interpretation = interpret_card(card, "upright", "general", tone)
    expected_prefix = TONE_PREFIXES[tone]
    assert interpretation.startswith(expected_prefix)


# Keywords should be separated with a comma in card order
def test_interpret_keywords_comma_separated(card):
    interpretation = interpret_card(card, "upright", "general", "mystic")
    keywords = card.keywords
    expected_keywords = ", ".join(keywords)
    assert expected_keywords in interpretation


# All full outputs should exactly match the template
@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("tone", TONES)
@pytest.mark.parametrize("orientation", ORIENTATIONS)
def test_interpret_exact_output(card, orientation, topic, tone):
    expected = EXPECTED_TEMPLATES[tone].format(
        meaning=meaning_for(card, orientation),
        context=TOPIC_CONTEXTS[topic],
        keywords=", ".join(card.keywords),
    )

    interpretation = interpret_card(card, orientation, topic, tone)
    assert interpretation == expected


# Same inputs should give same output
@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("tone", TONES)
@pytest.mark.parametrize("orientation", ORIENTATIONS)
def test_interpret_is_deterministic(card, orientation, topic, tone):
    interpretation1 = interpret_card(card, orientation, topic, tone)
    interpretation2 = interpret_card(card, orientation, topic, tone)
    assert interpretation1 == interpretation2


# Every card should work in all orientations
@pytest.mark.parametrize("orientation", ORIENTATIONS)
@pytest.mark.parametrize("deck_card", DECK, ids=lambda card: card.name)
def test_interpret_works_in_all_orientations(deck_card, orientation):
    interpretation = interpret_card(deck_card, orientation, "general", "mystic")
    assert meaning_for(deck_card, orientation) in interpretation
    assert ", ".join(deck_card.keywords) in interpretation


# Every topic and tone combination should work
@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("tone", TONES)
def test_interpret_works_for_all_topic_tone_combinations(topic, tone):
    for deck_card in DECK:
        interpretation = interpret_card(deck_card, "upright", topic, tone)
        assert TOPIC_CONTEXTS[topic] in interpretation
        assert interpretation.startswith(TONE_PREFIXES[tone])


# Card shouldn't be changed
def test_interpret_card_does_not_change_card(card):
    before = (card.name, card.upright, card.reversed, tuple(card.keywords))
    interpret_card(card, "upright", "general", "mystic")
    after = (card.name, card.upright, card.reversed, tuple(card.keywords))
    assert before == after


# Unsupported option values should raise ValueErrors
@pytest.mark.parametrize(
    "orientation",
    ["invert", "down", "sideways", " ", ""],
)
def test_interpret_invalid_orientation(card, orientation):
    with pytest.raises(ValueError):
        interpret_card(card, orientation, "general", "mystic")


@pytest.mark.parametrize(
    "topic",
    ["pizza", "happiness", "asdj", " ", ""],
)
def test_interpret_invalid_topic(card, topic):
    with pytest.raises(ValueError):
        interpret_card(card, "upright", topic, "mystic")


@pytest.mark.parametrize(
    "tone",
    ["happy", "sad", "sawki", " ", ""],
)
def test_interpret_invalid_tone(card, tone):
    with pytest.raises(ValueError):
        interpret_card(card, "upright", "general", tone)


# Option names are case sensitive and whitespace sensitive
@pytest.mark.parametrize(
    "orientation,topic,tone",
    [
        # bad orientation
        ("Upright", "general", "mystic"),
        ("REVERSED", "general", "mystic"),
        (" upright", "general", "mystic"),
        ("reversed ", "general", "mystic"),
        # bad tone
        ("upright", "general", "Mystic"),
        ("upright", "general", "FUNNY "),
        ("upright", "general", " programmer"),
        ("upright", "general", " funny"),
        # bad topic
        ("upright", "LOVE", "mystic"),
        ("upright", "career ", "mystic"),
        ("upright", " study", "mystic"),
        ("upright", "Money", "mystic"),
    ],
)
def test_interpret_case_and_whitespace_sensitivity(card, orientation, topic, tone):
    with pytest.raises(ValueError):
        interpret_card(card, orientation, topic, tone)


# Card must be Card instance
@pytest.mark.parametrize(
    "invalid_card",
    ["not a card", [], {}, "The Fool", 123, None],
)
def test_interpret_card_must_be_card_instance(invalid_card):
    with pytest.raises(TypeError):
        interpret_card(invalid_card, "upright", "general", "mystic")


# Options should be Strings
@pytest.mark.parametrize(
    "invalid_option",
    [123, None, [], {}, b"funny"],
)
def test_interpret_tone_must_be_string(card, invalid_option):
    with pytest.raises(TypeError):
        interpret_card(card, "upright", "general", invalid_option)


@pytest.mark.parametrize(
    "invalid_option",
    [123, None, [], {}, b"upright"],
)
def test_interpret_orientation_must_be_string(card, invalid_option):
    with pytest.raises(TypeError):
        interpret_card(card, invalid_option, "general", "mystic")


@pytest.mark.parametrize(
    "invalid_option",
    [123, None, [], {}, b"general"],
)
def test_interpret_topic_must_be_string(card, invalid_option):
    with pytest.raises(TypeError):
        interpret_card(card, "upright", invalid_option, "mystic")


# Type Errors should come before value errors
def test_interpret_card_type_error_before_value_error(card):
    with pytest.raises(TypeError):
        interpret_card(card, "sideways", None, "mystic")


def test_interpret_card_type_error_before_bad_options(card):
    with pytest.raises(TypeError):
        interpret_card("not a card", "sideways", "tissue", "strawberries")
