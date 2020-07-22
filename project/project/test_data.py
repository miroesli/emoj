import db_handler
import time
ranks = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine","ten", "jack", "queen", "king"]
suits = ["clubs", "hearts", "diamonds", "spades"]

for suit in suits:
    for rank in ranks:
        db_handler.insert_card(rank + " of " + suit, None, rank + "_" + suit)

cards = db_handler.get_cards()
decks = db_handler.get_template_decks("36e3531e-cc52-11ea-b508-784f437b7506")
for deck in decks:
    for card in cards:
        db_handler.insert_card_into_deck(deck.deck_uid, card.card_uid)
