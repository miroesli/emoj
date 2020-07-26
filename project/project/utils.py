from project import db_handler
from django.http import HttpResponse
import random

# After an item  is selected scan for what possible functions are supported by the current
# combination of selected options.


def display_options(room_uid, player_uid, selected):
    # enrich selected with player info
    for i in range(len(selected.get('players'))):
        player = db_handler.get_player(room_uid, selected.get('players')[i])
        if player:
            selected.get('players')[i] = player
        else:
            pass  # throw error

    # enrich selected with card info
    for i in range(len(selected.get('cards'))):
        card = db_handler.get_card(selected.get('cards')[i])
        if card:
            selected.get('cards')[i] = card
        else:
            pass  # throw error

    # if there is more than 1 location selected there are no options
    if len(selected.get('locations')) > 1:
        return []
    elif len(selected.get('locations')) == 1:
        # gets cards at location
        location_cards = db_handler.get_location_cards(
            room_uid, selected.get('locations')[0])
        # if an empty location selected
        if len(location_cards) == 0:
            # if the only thing selected is an empty location then we have no options
            # also if there is a player and empty location selected we also have no options
            if len(selected.get('cards')) == 0 or len(selected.get('players')) > 0:
                return []
            # empty location and cards selected
            else:

                pass  # place cards revealed or not revealed
        # non empty location selected
        else:
            # if we also select a player
            if len(selected.get('players')) > 0:
                # deal that player a card(for each revealed) + deal player X hidden cards
                pass
            # only non empty location selected
            else:
                # draw a card(for each revealed) + draw player X hidden cards
                pass
    # zero locations
    else:
        # player selected
        if len(selected.get('players')) > 0:
            if len(selected.get('cards')) > 0:
                # at least one player, card and location selected
                if len(selected.get('locations')) > 0:
                    return []
                else:
                    if len(selected.get('cards')) == 1 and len(selected.get('players')) == 1:
                        result = []
                        return ["give all to " + selected.get('players')[0].display_name]
        # only cards are selected
        else:
            result = []
            for card in selected.get('cards'):
                if not card.revealed:
                    result.append({"option": "reveal", "card_uid": card.card_uid,
                                   "option_text": "reveal " + card.card_name})
            return result

    return response


# This is the function handler to be called by api.py to pass all the json data from the axios request from the front end.
# It is to verify that the necessary data is requried before passing it on to the necessary function.
def function_handler(room_uid, player_uid, option, selected):
    pass


def reset_room(room_uid):
    db_handler.clear_cards_in_play(room_uid)
    db_handler.load_cards_in_play(room_uid)


def deal_card(room_uid, player_uid, game_board_location):
    card_uids = db_handler.draw_game_board_location_top_card(
        room_uid, game_board_location)
    card_uid = random.choice(card_uids)
    db_handler.update_card_location(room_uid, card_uid, None, player_uid)


def transfer_card(room_uid, entity_type1, entity_type2, entity_id1, entity_id2):
    if entity_type1 not in ['card', 'player', 'location']:
        pass  # throws err
    elif entity_type2 not in ['card', 'player', 'location']:
        pass  # throws err
    room = db_handler.get_room(room_uid)
