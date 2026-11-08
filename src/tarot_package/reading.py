from datetime import date
from .models import Card
from .interpret import interpret_card
from .draw import draw_cards
from .extras import lucky_extras

POSITIONS = ('Past', 'Present', 'Future')
TOPICS = ('love', 'career', 'study', 'money', 'general')
TONES = ('mystic', 'funny', 'programmer')

_SUMMARY = {
    "mystic": "I see {past} going through {present} and towards {future}. {mood}",
    "funny": "Plot twist: {past}, then {present}, and finally {future}. {mood}",
    "programmer": "Pipeline: {past} -> {present} -> {future}. {mood}",
}

_MOOD = {
    "mystic":(
        "A smooth and unbroken path is unfolding.",
        "A lingering darkness is present, but it can be overcome.",
        "Be patient with the universe; the stars are aligning the best they can."
    ),
    "funny":(
        "It's going flawlessly, don't make any sudden movements.",
        "One little plot twist on the horizon.",
        "Life has got a lot planned; enjoy the ride and bring snacks."
    ),
    "programmer":(
        "All unit tests successfully passed.",
        "A bug is lurking, but never fear, it can be fixed.",
        "Keep debugging and iterating; progress will come."
    ),     
}

def interpret_spread(
        
    drawn: list[tuple[Card, str]],
    topic: str = 'general',
    tone: str = 'mystic',

) -> str:
    """Interpret a three-card Past, Present, Future spread."""

    if len(drawn) != len(POSITIONS):
        raise ValueError("The number of drawn cards must match the number of positions.")
    if topic not in TOPICS:
        raise ValueError(f"Invalid topic: {topic}")
    if tone not in TONES:
        raise ValueError(f"Invalid tone: {tone}")


    card_texts = []
    for i in range(len(drawn)):
        position = POSITIONS[i]
        card = drawn[i][0]
        orientation = drawn[i][1]

        text = interpret_card(card, orientation, topic, tone)
        card_texts.append(position + ": " + card.name + " (" + orientation + ")\n" + text)

    reversed_num = 0
    for pair in drawn:
        if pair[1] == "reversed":
            reversed_num += 1

    # Determines the mood based on the number of reversed cards
    if reversed_num == 0:
        mood = _MOOD[tone][0]
    elif reversed_num == 1:
        mood = _MOOD[tone][1]
    else:
        mood = _MOOD[tone][2]

   
    summary = _SUMMARY[tone].format(
        past=drawn[0][0].keywords[0],
        present=drawn[1][0].keywords[0],
        future=drawn[2][0].keywords[0],
        mood=mood
    )
    return "\n\n".join(card_texts) + "\n\nSummary: " + summary




def daily_reading(
    name: str,
    date: date | None = None,
    topic: str = "general",
    tone: str = "mystic",
) -> str:
    """Generate a complete daily tarot reading."""
    drawn = draw_cards(name, date = date, count = 3)
    spread = interpret_spread(drawn, topic, tone)
    extras_color = lucky_extras(drawn, "color")
    extras_number = lucky_extras(drawn, "number")
    extras_advice = lucky_extras(drawn, "advice")
    return f"Reading for {name}\n\n{spread}\n\n{extras_color}\n{extras_number}\n{extras_advice}"
