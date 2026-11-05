from tarot_package import extras
from tarot_package.cards_major import MAJOR
from tarot_package.cards_cups import CUPS
from tarot_package.cards_pentacles import PENTACLES
from tarot_package.cards_swords import SWORDS
from tarot_package.data import lookup_card

fool = lookup_card("The Fool")
magician = lookup_card("The Magician")
two_cups = lookup_card("Two of Cups")
three_swords = lookup_card("Three of Swords")
ace_pent = lookup_card("Ace of Pentacles")

for card in [fool, magician, two_cups, three_swords, ace_pent]:
    drawn = [(card, "upright")]
    print(card.name, extras.lucky_extras(drawn, "color"), 
          extras.lucky_extras(drawn, "number"), extras.lucky_extras(drawn, "advice"))

print(extras.lucky_extras([(fool, "upright")], "color"))
print(extras.lucky_extras([(fool, "upright")], "number"))
print(extras.lucky_extras([(fool, "upright")], "advice"))

print(extras.lucky_extras([(fool, "reversed")], "color"))
print(extras.lucky_extras([(fool, "reversed")], "number"))
print(extras.lucky_extras([(fool, "reversed")], "advice"))

for bad_card, bad_category in [([], "color"), ([(fool, "upright")], "poach")]:
    try:
        extras.lucky_extras(bad_card, bad_category)
    except ValueError as e:
        print("ValueError: ",e)