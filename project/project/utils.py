from project import db_handler
from django.http import HttpResponse
import random

# Dictionary of functions with their tags.
functions = {
    'reset': reset_room,
    'deal': deal_card,
    'transfer': transfer_card,
}

# After an item  is selected scan for what possible functions are supported by the current
# combination of selected options.
def display_options(data):
    # TODO: selecting options handler function where if more than two things are selected
    response = HttpResponse()

    #Response should be json with the id/tag of the different options.
    response.status_code = 404
    
    return response



# This is the function handler to be called by api.py to pass all the json data from the axios request from the front end.
# It is to verify that the necessary data is requried before passing it on to the necessary function.
def function_handler(data):
    response = HttpResponse()

    # Check if the data includes a function tag.
    if 'tag' in data.keys():
        function = data['tag']
    else:
        response.status_code = 400
        response.content = 'No function provided'

    # Check if the requested function has been implemented.
    if function in functions.keys():
        #TODO: get http response from those functions
        functions[function](data)
    else:
        response.status_code = 404
        response.content = 'No such implemented function'

    return response



def reset_room(room_uid):
    db_handler.clear_cards_in_play(room_uid)
    db_handler.load_cards_in_play(room_uid)


def deal_card(room_uid, player_uid, game_board_location):
    card_uids = db_handler.draw_game_board_location_top_card(room_uid, game_board_location)
    card_uid = random.choice(card_uids)
    db_handler.update_card_location(room_uid, card_uid, None, player_uid)


def transfer_card(room_uid, entity_type1, entity_type2, entity_id1, entity_id2):
    if entity_type1 not in ['card', 'player', 'location']:
        pass #throws err
    if entity_type2 not in ['card', 'player', 'location']:
        pass #throws err
    else:
        pass #do stuff