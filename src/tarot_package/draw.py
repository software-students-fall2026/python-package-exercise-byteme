from datetime import date as Date, datetime
import json
from random import Random

from .data import DECK
from .models import Card


def draw_cards(
    name: str,
    date: Date | None = None,
    count: int = 3,
    allow_reversed: bool = True,
) -> list[tuple[Card, str]]:
    """Draw unique cards using a name and calendar date as the seed.

    Surrounding name whitespace is ignored; names are case-sensitive.
    If date is omitted, use today's local date. Count must be between
    one and the deck size. Orientations are "upright" or "reversed".
    This function does not change Python's global random state.

    Raises:
        TypeError: if an argument has the wrong type.
        ValueError: if name is blank or count is outside the deck's range.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    name = name.strip()
    if not name:
        raise ValueError("name must not be empty")
    if date is None:
        date = Date.today()
    elif not isinstance(date, Date) or isinstance(date, datetime):
        raise TypeError("date must be a datetime.date or None")
    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("count must be an integer")
    if not 1 <= count <= len(DECK):
        raise ValueError(f"count must be between 1 and {len(DECK)}")
    if not isinstance(allow_reversed, bool):
        raise TypeError("allow_reversed must be a boolean")

    # JSON keeps the two seed components separate without using hash(),
    # whose result can change between Python processes.
    seed = json.dumps([name, date.isoformat()], ensure_ascii=True)
    rng = Random(seed)
    cards = rng.sample(DECK, count)
    return [
        (card, rng.choice(("upright", "reversed")) if allow_reversed else "upright")
        for card in cards
    ]
