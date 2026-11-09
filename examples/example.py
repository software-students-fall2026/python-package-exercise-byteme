"""Example program that uses every function in the tarot package.

Run from the repository root with:
    python3 -m pip install -e .
    python3 examples/example.py
"""

from datetime import date

from tarot_package import (
    interpret_spread, 
    daily_reading, 
    interpret_card,
    draw_cards,
    lucky_extras,
    lookup_card,
)

TOPICS = ("love", "career", "study", "money", "general")
TONES = ("funny", "mystic", "programmer")
CATEGORIES = ("color", "number", "advice")

NAME = "Uuree"
DAY = date(2026, 11, 8)
LINE = "-" * 63

def section(title):
    print(f"\n{LINE}\n{title}\n{LINE}")

section("draw_cards(allow_reversed=True)")
drawn = draw_cards(NAME, date=DAY, count=3, allow_reversed=True)
for card, orientation in drawn:
    print(f"{card.name} ({orientation})")

section("draw_cards(allow_reversed=False): every card is upright")
upright_drawn = draw_cards(NAME, date=DAY, count=3, allow_reversed=False)
for card, orientation in upright_drawn:
    print(f"{card.name} ({orientation})")

section("lookup_card: exact name, a typo, and keyword")
print(lookup_card("The Fool").name)
print(lookup_card("the magicain").name)
print(lookup_card("inner voice").name)

section("interpret_card: both orientations")
fool = lookup_card("The Fool")
print(interpret_card(fool, "upright", "love", "funny"))
print(interpret_card(fool, "reversed", "love", "funny"))

section("interpret_card: every topic")
for topic in TOPICS:
    print(f"[{topic}]\n{interpret_card(fool, 'upright', topic, 'mystic')}")
    print()

section("interpret_spread: every tone")
for tone in TONES:
    print(f"[{tone}]\n{interpret_spread(drawn, topic='career', tone=tone)}")
    print()

section("lucky_extras: every category")
for category in CATEGORIES:
    print(f"[{category}]\n{lucky_extras(drawn, category)}")

section("daily_reading: default")
print(daily_reading(NAME, date=DAY))

section("daily_reading: topic = 'love', tone = 'funny'")
print(daily_reading(NAME, date=DAY, topic="love", tone="funny"))
