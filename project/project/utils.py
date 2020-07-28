from project import db_handler
from django.http import HttpResponse
import random
from collections import deque
# After an item  is selected scan for what possible functions are supported by the current
# combination of selected options.


def display_options(room_uid, player_uid, selected):
    # enrich selected with player info
    for i in range(len(selected.get('players'))):
        player = db_handler.get_player(selected.get('players')[i], room_uid)
        if player:
            selected.get('players')[i] = player
        else:
            pass  # throw error

    # enrich selected with card info
    for i in range(len(selected.get('cards'))):
        card = db_handler.get_room_card(selected.get('cards')[i], room_uid)
        if card:
            selected.get('cards')[i] = card
        else:
            pass  # throw error

    # if there is more than 1 location selected there are no options
    if len(selected.get('locations')) > 1:
        return []
    elif len(selected.get('locations')) == 1:
        # gets cards at location
        location_cards = db_handler.get_location_cards(room_uid, selected.get('locations')[0][0], selected.get('locations')[0][1])
        # if an empty location selected
        if len(location_cards) == 0:
            # if the only thing selected is an empty location then we have no options
            # also if there is a player and empty location selected we also have no options
            if len(selected.get('cards')) == 0 or len(selected.get('players')) > 0:
                return []
            # empty location and cards selected
            else:
                return [{"option": "place revealed", "option_text": "place selected card(s) face up"},
                        {"option": "place", "option_text": "place selected card(s) face down"}]
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
        if len(selected.get('players')) > 1:
            return []
        elif len(selected.get('players')) == 1:
            if len(selected.get('cards')) > 0:
                return [{"option": "give",
                         "option_text": "give selected card(s) to " + selected.get('players')[0].display_name}]
            # only a player is selected so we can pass them the turn
            else:
                return [{"option": "pass", "option_text": "pass turn to " + selected.get('players')[0].display_name}]
        # only cards are selected
        else:
            result = []
            for card in selected.get('cards'):
                if not card.revealed:
                    result.append({"option": "reveal", "option_text": "reveal " + card.card_name})
            return result


# This is the function handler to be called by api.py to pass all the json data from the axios request from the front end.
# It is to verify that the necessary data is requried before passing it on to the necessary function.
#todo location stuff
def function_handler(room_uid, player_uid, option, selected):

    posible_options = ["reveal", "pass", "give", "place revealed", "place"]
    if option not in posible_options:
        pass #throw error
    player = db_handler.get_player(player_uid, room_uid)
    if option == "reveal":
        for i in selected.get('cards'):
            db_handler.reveal_card(room_uid, player_uid, i)
            card = db_handler.get_card(i)
            db_handler.log_action(room_uid, player.display_name+" reveals "+ card.card_name)
    elif option == "pass":
        db_handler.pass_turn(room_uid, player_uid, selected.get('players')[0])
        p2 = db_handler.get_player(selected.get('players')[0], room_uid)
        db_handler.log_action(room_uid, player.display_name+" passes the turn to "+ p2.display_name)
    elif option == "give":
        p2 = db_handler.get_player(selected.get('players')[0], room_uid)
        for i in selected.get('cards'):
            db_handler.give_card(room_uid, player_uid, selected.get('players'[0]),i)
            card = db_handler.get_card(i)
            db_handler.log_action(room_uid, player.display_name+" gave "+ card.card_name + " to "+ p2.display_name)
    elif option =="place revealed":
        pass
    else:
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


# made to refresh page status using API
def load_play_info(room_uid, player_uid):
    room = db_handler.get_room(room_uid)
    player = db_handler.get_player(player_uid, room_uid)
    room_players = db_handler.get_room_players(room_uid)
    player_index = None
    for index, player in enumerate(room_players):
        if str(player.player_uid) == player_uid:
            player_index = index
            break
    # if not player_index:
    #     # TODO: implement
    #     db_handler.add_player_to_room(room_uid, player_uid)
    #     room_players = db_handler.get_room_players(room_uid)
    room_players = deque(room_players)
    room_players.rotate(player_index)  # moving list to correct order
    room_players = list(room_players)
    # removing current players from room_players
    room_players = room_players[1:]

    player.hand = [i.to_dict() for i in db_handler.get_player_cards(
        player.player_uid, room_uid)]
    for p in room_players:
        p.hand = db_handler.get_player_card_revealed(
            p.player_uid, room_uid)
        p.card_count = db_handler.get_player_card_count(
            p.player_uid, room_uid)

    template = db_handler.get_room_template(room_uid)
    template.decks = db_handler.get_template_decks(template.template_uid)
    for deck in template.decks:
        deck.game_board_location = str(deck.game_board_location.x) + str(deck.game_board_location.y)

    return {"player": player.to_dict(), "players": [i.to_dict() for i in room_players], "room": room,
            "template": template.to_dict()}
