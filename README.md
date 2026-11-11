# Daily Tarot Card Readings

[![Build and Test](https://github.com/software-students-fall2026/python-package-exercise-byteme/actions/workflows/test.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-byteme/actions/workflows/test.yml)

A light-hearted Python package that draws a three-card tarot reading (Past, Present, and Future) and interprets it. Give it a name and a date, and it deals three unique cards from a 78-card deck. Each card may be upright or reversed. The reading can be altered by topic (love, career, study, money, general) and tone (mystic, funny, programmer). The same name and date will always give the same cards.

**PyPI:** https://pypi.org/project/byteme-tarot/

**Task board:** https://github.com/orgs/software-students-fall2026/projects/95

## Team members

- [Tracy Wang](https://github.com/TracyWang0904)
- [Emma Ao](https://github.com/emma6594)
- [Jingjing Wang](https://github.com/JingjingWang129)
- [Uuriintuya Ganzorig](https://github.com/Uuriii1003)

## Installation

Requires **Python 3.11 or newer**.

```bash
pip install byteme-tarot
```

If `pip` isn't found, use `python3 -m pip install byteme-tarot`

Then import it in your own code:

```python
from tarot_package import daily_reading

print(daily_reading("Emma", topic="love", tone="funny"))
print(daily_reading("Uuree"))
```

## Contributing

On Windows, use `python` or `py` in place of `python3`. If pipenv isn't found, run `python -m pipenv`

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-byteme.git
cd python-package-exercise-byteme
python3 -m pip install pipenv
pipenv install --dev
pipenv run python -m pytest tests/
pipenv run python -m build
```

If pipenv can't find the right Python, run `pipenv --python python3 install --dev`. 

To run a single test file:

```bash
pipenv run python -m pytest tests/test_lookup.py -v
```

Every pull request is built and tested on Python 3.10, 3.11, and 3.12 by GitHub Actions.

## Example Program

See [`examples/example.py`](https://github.com/software-students-fall2026/python-package-exercise-byteme/blob/main/examples/example.py), which uses every function in the package.

**If you cloned the repository**, install the package first, then run the example from the repository root:

```bash
python3 -m pip install -e .
python3 examples/example.py
```

**If you installed from PyPI**, run:

```bash
curl -O https://raw.githubusercontent.com/software-students-fall2026/python-package-exercise-byteme/main/examples/example.py
python3 example.py
```

## Functions

### `lookup_card(query)`
Finds a card by name or keyword, where small typos are forgiven. Raises `ValueError` if nothing matches and `TypeError` if `query` isn't a string

```python
from tarot_package import lookup_card

print(lookup_card("the fool").name)
```
Output:
```text
The Fool
```

### `draw_cards(name, date=None, count=3, allow_reversed=True)`
Draws unique cards from the 78 card deck and each draw is seeded by `name` and `date`, so the same person on the same day gets the same cards. Returns a list of (Card, orientation)

```python
from datetime import date
from tarot_package import draw_cards

drawn = draw_cards("Jingjing", date=date(2026, 11, 8))
for card, orientation in drawn:
    print(f"{card.name} ({orientation})")
```
Output:
```text
Four of Wands (reversed)
Five of Pentacles (reversed)
The Devil (reversed)
```

### `interpret_card(card, orientation, topic, tone)`
Interprets a single card by phrasing its upright or reversed meaning for the chosen topic and tone, returning a String. Raises a TypeError for non-string input or ValueError if an option is unsupported.

```python
from tarot_package import lookup_card, interpret_card

card = lookup_card("The Fool")
print(interpret_card(card, "upright", "love", "funny"))
```
Output:
```text
Your tarot plot twist: A fresh start is calling, so take the leap with an open heart. For your relationships, keep beginnings, innocence, adventure, spontaneity on the guest list. Bring snacks.
```

### `interpret_spread(drawn, topic="general", tone="mystic")`
Interprets Past, Present, and Future, plus a summary of the drawn 3 cards, returning a String.

```python
from datetime import date
from tarot_package import draw_cards, interpret_spread

drawn = draw_cards("Tracy", date=date(2026, 11, 8))
print(interpret_spread(drawn, topic="career", tone="programmer"))
```
Output:
```text
Past: Two of Wands (reversed)
Card output: Fear of the unknown keeps you in your comfort zone, so plan one bold step. For your work and career, debug your next step with these keywords: planning, decisions, vision, ambition.

Present: The High Priestess (upright)
Card output: Stay quiet and listen, because your intuition knows more than you think. For your work and career, debug your next step with these keywords: intuition, mystery, secrets, inner voice.

Future: Ten of Pentacles (reversed)
Card output: Money disputes or shaky foundations need attention before they grow. For your work and career, debug your next step with these keywords: legacy, family, wealth, long-term.

Summary: Pipeline: planning -> intuition -> legacy. Keep debugging and iterating; progress will come.
```

### `lucky_extras(drawn, category)`
Categories: `"color"`, `"number"`, `"advice"`
Returns a lucky color, number, or advice based on the drawn cards. Raises a ValueError for an invalid category.

```python
from datetime import date
from tarot_package import draw_cards, lucky_extras

drawn = draw_cards("Emma", date=date(2026, 11, 8))
print(lucky_extras(drawn, "color"))
print(lucky_extras(drawn, "number"))
print(lucky_extras(drawn, "advice"))
```
Output:
```text
Lucky color: green
Lucky number: 8
Consider the potential impact of diligence on your well-being.
```

### `daily_reading(name, date=None, topic="general", tone="mystic")`
Returns a full daily reading including interpretation of each card, interpretation of all 3 together, and lucky color, number, and advice.

```python
from datetime import date
from tarot_package import daily_reading

print("Default (mystic tone)")
print(daily_reading("Uuree", date=date(2026, 11, 8)))
print()
print("Love topic, funny tone")
print(daily_reading("Uuree", date=date(2026, 11, 8), topic="love", tone="funny"))
```
Output:
```text
Default (mystic tone)
Reading for Uuree

Past: Knight of Swords (upright)
The cards whisper: Quick, bold action pushes things forward, but mind your tone. In your daily life, let these themes guide your reflection: speed, ambition, bluntness, drive.

Present: Two of Pentacles (upright)
The cards whisper: You are juggling a lot, so stay flexible and keep your priorities straight. In your daily life, let these themes guide your reflection: balance, juggling, adaptability, priorities.

Future: The Tower (reversed)
The cards whisper: You are dodging an upheaval that needs to happen sooner or later. In your daily life, let these themes guide your reflection: upheaval, shock, revelation, collapse.

Summary: I see speed going through balance and towards upheaval. A lingering darkness is present, but it can be overcome.

Lucky color: yellow
Lucky number: 6
Be mindful of how upheaval affects your choices.

Love topic, funny tone
Reading for Uuree

Past: Knight of Swords (upright)
Your tarot plot twist: Quick, bold action pushes things forward, but mind your tone. For your relationships, keep speed, ambition, bluntness, drive on the guest list. Bring snacks.

Present: Two of Pentacles (upright)
Your tarot plot twist: You are juggling a lot, so stay flexible and keep your priorities straight. For your relationships, keep balance, juggling, adaptability, priorities on the guest list. Bring snacks.

Future: The Tower (reversed)
Your tarot plot twist: You are dodging an upheaval that needs to happen sooner or later. For your relationships, keep upheaval, shock, revelation, collapse on the guest list. Bring snacks.

Summary: Plot twist: speed, then balance, and finally upheaval. One little plot twist on the horizon.

Lucky color: yellow
Lucky number: 6
Be mindful of how upheaval affects your choices.
```

**Valid options**
- Topics: `love`, `career`, `study`, `money`, `general`
- Tones: `mystic`, `funny`, `programmer`

## Configuration

No "secret" configuration files, env variables, or databases are needed.
