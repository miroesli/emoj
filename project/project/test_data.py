from project import db_handler
import time
ranks = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine","ten", "jack", "queen", "king"]
suits = ["clubs", "hearts", "diamonds", "spades"]

for suit in suits:
    for rank in ranks:
        db_handler.insert_card(rank + " of " + suit, None, rank + "_" + suit)

