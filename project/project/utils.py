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

    if len(selected.get('locations')) > 2:
        return []
    # multiple locations
    if len(selected.get('locations')) == 2:
        if len(selected.get('players'))>0 or len(selected.get('cards'))>0:
            return []
        else:
            non_empty = 0
            for location in selected.get('locations'):
                location_cards = db_handler.get_location_cards(room_uid, location.get('x'), location.get('y'))
                if len(location_cards) > 0:
                    non_empty+=1

            if non_empty == 1:
                return [{"option": "deal location revealed", "option_text": "deal from selected deck face up"},
                        {"option": "deal location", "option_text": "deal from selected deck face down"}]
            else:
                return []
    elif len(selected.get('locations')) == 1:
        # gets cards at location
        location_cards = db_handler.get_location_cards(room_uid, selected.get('locations')[0].get('x'),
                                                       selected.get('locations')[0].get('y'))
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
            if len(selected.get('players')) > 0 and len(selected.get('cards')) == 0:
                # deal that player a card(for each revealed) + deal player X hidden cards
                k = min(7 - len(selected.get('players')), len(location_cards))
                return ([{"option": "deal", "quantity": i,
                            "option_text": "deal "+str(i)+" card(s) to "+p.display_name}
                        for p in selected.get('players') for i in range(1,k)])
            # only non empty location selected
            elif len(selected.get('players')) == 0:
                # draw a card(for each revealed) + draw player X hidden cards
                k = min(6, len(location_cards))
                return [{"option": "draw", "quantity": i, "option_text": "draw "+str(i)+" card(s)"} for i in range(1, k)]
            else:
                return []
    # zero locations
    else:
        # player selected
        if len(selected.get('players')) > 1:
            return []
        elif len(selected.get('players')) == 1:
            if len(selected.get('cards')) > 0:
                return [{"option": "give",
                         "option_text": "give selected card(s) to " + selected.get('players')[0].display_name},
                        {"option": "give revealed",
                         "option_text": "reveal and give selected card(s) to " + selected.get('players')[0].display_name}]
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

    posible_options = ["reveal", "pass", "give revealed", "give", "place revealed", "place", "deal", "draw",
                       "deal location", "deal location revealed"]
    if option not in posible_options:
        raise LookupError("option not found" + option)
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
    elif option == "give" or option == "give revealed":
        p2 = db_handler.get_player(selected.get('players')[0], room_uid)
        for i in selected.get('cards'):
            db_handler.give_card(room_uid, player_uid, selected.get('players')[0], i)
            if option == "give revealed":
                card = db_handler.get_card(i)
                db_handler.log_action(room_uid, player.display_name+" gave "+ card.card_name + " to " + p2.display_name)
        if option != "give revealed":
            db_handler.log_action(room_uid, player.display_name+" gave a card to " + p2.display_name)
    elif option == "place revealed" or option == "place":
        for card_uid in selected.get('cards'):
            card = db_handler.get_card(card_uid)
            transfer_card(room_uid,card.card_uid,"location",selected.get('locations')[0],True)
            if option == "place revealed":
                db_handler.log_action(room_uid,player.display_name + " placed " + card.card_name)
        if option == "place":
            db_handler.log_action(room_uid, player.display_name + " placed " + str(len(selected.get('cards'))) + " card(s)")
    elif option == "deal":
        for i in range(option.get('quantity')):
            deal_card(room_uid,selected.get('players')[0].player_uid, selected.get('locations')[0])
            #db_handler.log_action(room_uid, player.display_name + " placed " + str(len(selected.get('cards'))) + " card(s)")
    elif option == "draw":
        pass
    elif option == "deal location":
        pass
    elif option == "deal location revealed":
        pass
    else:
        raise LookupError("option not found")


def reset_room(room_uid):
    db_handler.clear_cards_in_play(room_uid)
    db_handler.clear_log(room_uid)
    db_handler.load_cards_in_play(room_uid)


def deal_card(room_uid, player_uid, game_board_location):
    card_uids = db_handler.draw_game_board_location_top_card(
        room_uid, game_board_location)
    card_uid = random.choice(card_uids)
    db_handler.update_card_location(room_uid, card_uid, None, player_uid)


def transfer_card(room_uid, card_uid, entity_type, entity_id):
    pass


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
    if not player_index:
        db_handler.insert_room_player(room_uid, player_uid)
        room_players = db_handler.get_room_players(room_uid)
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

    positions = [{'x': i, 'y': j} for i in range(4) for j in range(6)]
    for i in template.decks:
        for p in positions:
            if p['x'] == i.game_board_location.x and p['y'] == i.game_board_location.y:
                p.update(i.to_dict())

    room_log = db_handler.get_room_log(room_uid)

    return {"player": player.to_dict(), "players": [i.to_dict() for i in room_players], "room": room.to_dict(),
            "template": template.to_dict(), "positions": positions, "room_log": room_log}
