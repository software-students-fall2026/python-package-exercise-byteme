# Daily Tarot Card Readings

[![Build and Test](https://github.com/software-students-fall2026/python-package-exercise-byteme/actions/workflows/test.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-byteme/actions/workflows/test.yml)

A light-hearted Python package that draws a three-card tarot reading (Past, Present, and Future) and interprets it. Give it a name and a date, and it deals three unique cards from a 78-card deck. Each card may be upright or reversed. The reading can be altered by topic (love, career, study, money, general) and tone (mystic, funny, programmer).

## Team members

- [Tracy Wang](https://github.com/TracyWang0904)
- [Emma Ao](https://github.com/emma6594)
- [Jingjing Wang](https://github.com/JingjingWang129)
- [Uuriintuya Ganzorig](https://github.com/Uuriii1003)

## Installation

Requires **Python 3.10 or newer**.

```bash
pip install byteme-tarot
```

Then import it in your own code:

```python
from tarot_package import daily_reading

print(daily_reading("Emma", topic = "love", tone = "funny"))
print(daily_reading("Uuree"))
```

## Contributing

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-byteme.git
cd python-package-exercise-byteme
python3 -m pip install pipenv

```

## Functions

### `draw_cards(name, date = None, count = 3, allow_reversed = True)`
Draws unique cards from the 78 card deck and each draw is seeded by `name` and `date`, so the same person on the same day gets the same cards. Returns a list of (Card, orientation)

```python
from datetime import date
from tarot_package import draw_cards

drawn = draw_cards("Jingjing", date = date(2026, 11, 8))
```

### `interpret_card(card, orientation, topic, tone)`
Interprets a single card by taking the card's upright or reverse meaning and returns a String. Raises a TypeError for non-string input

```python
from tarot_package import lookup_card, interpret_card

card = lookup_card("The Fool")
print(interpret_card(card, "upright", "love", "funny"))
```

### `interpret_spread(drawn, topic, tone)`
Interprets Past, Present, and Future, plus a summary of the drawn 3 cards

```python
from tarot_package import draw_cards, interpret_spread

drawn = draw_cards("Tracy")
print(interpret_spread(drawn, topic = "career", tone = "programmer"))
```

### `lucky_extras(drawn, category)`
Categories: `"color"`, `"number"`, `"advice"`
Returns a lucky color, number, or advice based on the drawn cards. Raises a ValueError for an invalid category.

```python
from tarot_package import draw_cards, lucky_extras

drawn = draw_cards("Emma")
print(lucky_extras(drawn, "color"))
print(lucky_extras(drawn, "number"))
print(lucky_extras(drawn, "advice"))
```

### `lookup_card(query)`
Finds a card by name or keyword, with fuzzy matching. Raises `ValueError` if nothing matches.

```python
from tarot_package import lookup_card

print(lookup_card("the fool").name)
print(lookup_card("the magicain").name)
```

### `daily_reading(name, date = None, topic = "general", tone = "mystic")`
Return a full daily reading including interpretation of each card, interpretation of all 3 together, and lucky color, number, and advice

```python
from tarot_package import daily_reading

print(daily_reading("Uuree"))
print(daily_reading("Uuree", topic = "love", tone = "funny"))
```


**Valid options**
- Topics: `love`, `career`, `study`, `money`, `general`
- Tones: `mystic`, `funny`, `programmer`

## Example Program

```bash
python3 examples/example.py
```

