# Tests for the interpret_spread function

from datetime import date

import pytest

from tarot_package import draw_cards, interpret_card, interpret_spread, lookup_card

TOPICS = ["love", "career", "study", "money", "general"]
TONES = ["mystic", "funny", "programmer"]


def make_spread(*orientations):
    names = ["The Fool", "Two of Cups", "Three of Swords"]
    return [(lookup_card(name), orientation) for name, orientation in zip(names, orientations)]


@pytest.fixture
def spread():
    return make_spread("upright", "reversed", "upright")


# The spread lists Past, Present, Future and a Summary in that order
def test_spread_has_all_sections_in_order(spread):
    result = interpret_spread(spread)

    positions = [result.index(label) for label in ("Past:", "Present:", "Future:", "Summary:")]
    assert positions == sorted(positions)


# Each position shows the card name and its orientation
def test_spread_shows_card_names_and_orientations(spread):
    result = interpret_spread(spread)

    assert "Past: The Fool (upright)" in result
    assert "Present: Two of Cups (reversed)" in result
    assert "Future: Three of Swords (upright)" in result


# Every topic and tone combination returns text
@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("tone", TONES)
def test_every_topic_and_tone_works(spread, topic, tone):
    result = interpret_spread(spread, topic, tone)

    assert isinstance(result, str)
    assert result.strip()


# The defaults are the general topic and the mystic tone
def test_defaults_are_general_and_mystic(spread):
    assert interpret_spread(spread) == interpret_spread(spread, "general", "mystic")


# Each card is interpreted with the chosen topic and tone
@pytest.mark.parametrize("tone", TONES)
def test_each_card_interpretation_is_included(spread, tone):
    result = interpret_spread(spread, "career", tone)

    for card, orientation in spread:
        assert interpret_card(card, orientation, "career", tone) in result


# The summary style follows the tone
@pytest.mark.parametrize(
    "tone,prefix",
    [("mystic", "I see "), ("funny", "Plot twist: "), ("programmer", "Pipeline: ")],
)
def test_summary_style_follows_tone(spread, tone, prefix):
    result = interpret_spread(spread, "general", tone)
    summary = result.split("Summary: ")[1]

    assert summary.startswith(prefix)


# The summary uses the first keyword of each card, in order
def test_summary_uses_first_keywords(spread):
    result = interpret_spread(spread, "general", "programmer")
    past, present, future = (card.keywords[0] for card, _ in spread)

    assert f"Pipeline: {past} -> {present} -> {future}." in result


# The closing mood depends on how many cards are reversed
@pytest.mark.parametrize(
    "orientations,mood",
    [
        (("upright", "upright", "upright"), "All unit tests successfully passed."),
        (("reversed", "upright", "upright"), "A bug is lurking, but never fear, it can be fixed."),
        (("upright", "reversed", "upright"), "A bug is lurking, but never fear, it can be fixed."),
        (("reversed", "reversed", "upright"), "Keep debugging and iterating; progress will come."),
        (("reversed", "reversed", "reversed"), "Keep debugging and iterating; progress will come."),
    ],
)
def test_mood_depends_on_reversed_count(orientations, mood):
    result = interpret_spread(make_spread(*orientations), "general", "programmer")

    assert result.endswith(mood)


# The same draw always gives the same text
def test_result_is_deterministic():
    drawn = draw_cards("Tracy", date=date(2026, 11, 8))

    assert interpret_spread(drawn, "love", "funny") == interpret_spread(drawn, "love", "funny")


# A real draw from draw_cards can be interpreted
def test_works_on_real_draw():
    drawn = draw_cards("Emma", date=date(2026, 11, 8))
    result = interpret_spread(drawn, "money", "mystic")

    for card, orientation in drawn:
        assert f"{card.name} ({orientation})" in result


# Exactly three cards are required
@pytest.mark.parametrize("count", [0, 1, 2, 4])
def test_wrong_number_of_cards(count):
    drawn = draw_cards("Tracy", date=date(2026, 11, 8), count=count) if count else []

    with pytest.raises(ValueError):
        interpret_spread(drawn)


# An unknown topic should raise ValueError
@pytest.mark.parametrize("topic", ["health", "", "LOVE", None])
def test_invalid_topic(spread, topic):
    with pytest.raises(ValueError):
        interpret_spread(spread, topic=topic)


# An unknown tone should raise ValueError
@pytest.mark.parametrize("tone", ["serious", "", "Funny", None])
def test_invalid_tone(spread, tone):
    with pytest.raises(ValueError):
        interpret_spread(spread, tone=tone)


# An invalid orientation in the draw should raise ValueError
def test_invalid_orientation(spread):
    bad = [(spread[0][0], "sideways"), spread[1], spread[2]]

    with pytest.raises(ValueError):
        interpret_spread(bad)


# Something that is not a Card in the draw should raise TypeError
def test_invalid_card_type(spread):
    bad = [("The Fool", "upright"), spread[1], spread[2]]

    with pytest.raises(TypeError):
        interpret_spread(bad)