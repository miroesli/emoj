from project import db_handler
from django.http import HttpResponse
import random

# options function where if more than two things are selected

# This is the function handler to be called by api.py to pass all the json data from the axios request from the front end.
# It is to verify that the necessary data is requried before passing it on to the necessary function.
def function_handler(data):
    response = HttpResponse()
    # Check if the data includes a function tag.
    if 'tag' in data.keys():
        function = data['tag']
    else:
        # TODO: if no tag exists return correct http response error for malformed data
        response.status_code = 400
        response.content = 'No tag provided'
        pass

    # TODO: loop over every possible function checking (replace with python switch statement equivalent)
    # if the require componenets are not included again return http response error for malformed data
    # if they are call those functions and pass the parameters

    # put the function into a dict, try and get the provided function and execute it.
    # if it ails return malformed data response
    if(function=='reset_room'):
        if 'room_uid' in data.keys():
            reset_room(data['room_uid'])
        else:
            # TODO: if the necessary keys are not in the ata throw http response error for malformed data
            pass
    

    

def reset_room(room_uid):
    db_handler.clear_cards_in_play(room_uid)
    db_handler.load_cards_in_play(room_uid)


def deal_card(room_uid, player_uid, game_board_location):
    card_uids = db_handler.draw_game_board_location_top_card(room_uid, game_board_location)
    card_uid = random.choice(card_uids)
    db_handler.update_card_location(room_uid, card_uid, None, player_uid)

# TODO: Function to transfer cards from one origin to one target.
# Called with origin and target type the other possible origin/target type set to None.
def transfer_card(room_uid, card_uid, origin_location, origin_player_uid, target_location, target_player_uid):

    # If multiple origins have been provided:
    if(origin_location!= None and origin_player_uid != None):
        # TODO: return a bad response for malformed data maybe with a string detailing too many origins
        pass
    # if mutliple targets have been provided
    if(target_location!= None and target_player_uid != None):
        pass

    # Check if the target card is actually at the origin
    if(origin_location != None):
        # TODO: check if the card is there and if it isn't throw a bad response
        pass
    elif(origin_player_uid!=None):
        # TODO: check if the card is there and if it isn't throw a bad response
        pass

    # TODO: db_handler Update card location to whichever target was used?


