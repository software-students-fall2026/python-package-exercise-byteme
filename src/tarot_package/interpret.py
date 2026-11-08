from .models import Card


_TOPIC_CONTEXTS = {
    "love": "your relationships",
    "career": "your work and career",
    "study": "your learning and studies",
    "money": "your money and resources",
    "general": "your daily life",
}

_TEMPLATES = {
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


def interpret_card(
    card: Card,
    orientation: str,
    topic: str,
    tone: str,
) -> str:
    """Wrap a card's meaning and keywords in a topic and tone template.

    Orientation must be "upright" or "reversed". Supported topics are
    love, career, study, money, and general; supported tones are mystic,
    funny, and programmer. Option names are case-sensitive.

    Raises:
        TypeError: if card is not a Card or an option is not a string.
        ValueError: if an option is unsupported.
    """
    if not isinstance(card, Card):
        raise TypeError("card must be a Card")
    for label, value in (
        ("orientation", orientation), ("topic", topic), ("tone", tone)
    ):
        if not isinstance(value, str):
            raise TypeError(f"{label} must be a string")
    if orientation not in ("upright", "reversed"):
        raise ValueError("orientation must be 'upright' or 'reversed'")
    if topic not in _TOPIC_CONTEXTS:
        raise ValueError(f"Invalid topic: {topic}")
    if tone not in _TEMPLATES:
        raise ValueError(f"Invalid tone: {tone}")

    meaning = card.upright if orientation == "upright" else card.reversed
    return _TEMPLATES[tone].format(
        meaning=meaning,
        context=_TOPIC_CONTEXTS[topic],
        keywords=", ".join(card.keywords),
    )
