from datetime import date

from .reading import interpret_spread, daily_reading
from .interpret import interpret_card
from .draw import draw_cards
from .extras import lucky_extras
from .data import lookup_card

print("\nDrawn cards:")
drawn = draw_cards("Jingjing", date = date(2026, 11, 8))
for card, orientation in drawn:
    print(card, orientation)
    print("\n")

print("\n-----------------------------------------------------------------------")

print("Interpretation of The Fool:")
card = lookup_card("The Fool")
print(interpret_card(card, "upright", "love", "funny"))

print("\n-----------------------------------------------------------------------")

print("\nInterpretation of spread:")
print(interpret_spread(drawn, topic = "career", tone = "programmer"))

print("\n-----------------------------------------------------------------------")

print("\nLucky extras:")
print(lucky_extras(drawn, "color"))
print(lucky_extras(drawn, "number"))
print(lucky_extras(drawn, "advice"))

print("\n-----------------------------------------------------------------------")

print("\nDaily reading:")
print(daily_reading("Jingjing"))
print(daily_reading("Jingjing", topic = "love", tone = "funny"))

print("\n-----------------------------------------------------------------------")