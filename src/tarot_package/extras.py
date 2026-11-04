from .models import Card

EXTRA_CATEGORIES = ("color", "number", "advice")

COLORS = {
    "wands": "red",
    "cups": "blue",
    "swords": "yellow",
    "pentacles": "green",
    None: "purple",
}

NUMBERS = {
    "wands": (3, 8, 9),
    "cups": (2, 4, 10),
    "swords": (1, 6, 10),
    "pentacles": (1, 4, 8),
    None: (2, 5, 7),
}

ADVICE_UPRIGHT = (
    "Notice where {kw} already appears in your life.",
    "Reflect on how {kw} influences your decisions.",
    "Consider how {kw} can guide your actions.",
    "Give {kw} more attention in your daily life."
)

ADVICE_REVERSED = (
    "Don't ignore the influence of {kw} in your life.",
    "Be mindful of how {kw} affects your choices.",
    "Consider the potential impact of {kw} on your well-being.",
    "Seek guidance from {kw} when facing challenges."
)

def lucky_extras(
    drawn: list[tuple[Card, str]],
    category: str,
) -> str:
    """Generate a lucky extra based on the drawn cards."""
    if category not in EXTRA_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    if len(drawn) == 0:
        raise ValueError("Must draw at least one card.")
    
    if category == "color":
        card = drawn[0][0]
        color = COLORS.get(card.suit, COLORS[None])
        return f'Lucky color: {color}'
    elif category == "number":
        card = drawn[0][0]
        options = NUMBERS.get(card.suit, NUMBERS[None])
        number = options[len(card.name) % len(options)]
        return f'Lucky number: {number}'
    elif category == "advice":
        card = drawn[-1][0]
        orientation = drawn[-1][1]
        if orientation == "upright":
            advice = ADVICE_UPRIGHT[len(card.name) % len(ADVICE_UPRIGHT)]
        else:
            advice = ADVICE_REVERSED[len(card.name) % len(ADVICE_REVERSED)]
        return advice.format(kw=card.keywords[0])

