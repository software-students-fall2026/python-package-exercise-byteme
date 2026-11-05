from tarot_package import reading
from tarot_package.cards_major import MAJOR
from tarot_package.cards_cups import CUPS
from tarot_package.cards_swords import SWORDS

def fake_interpret_card(card, orientation, topic, tone):
    if orientation == 'upright':
        return card.upright
    else:
        return card.reversed

reading.interpret_card = fake_interpret_card

drawn = [
    (SWORDS[0], 'upright'),
    (CUPS[2], 'reversed'),
    (MAJOR[1], 'upright'),
]

print(reading.interpret_spread(drawn, "love", "mystic"))