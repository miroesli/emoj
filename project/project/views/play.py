from django.shortcuts import render, redirect
from project import db_handler, utils
from django.contrib.auth.models import Permission, User
from collections import deque


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


# example of uid 36e37bb4-cc52-11ea-b508-784f437b7506
def render_play(request, room_uid):
    room = db_handler.get_room(room_uid)
    if not room:
        return redirect('/')
    else:
        utils.reset_room(room_uid)
        # replace with get room players when data is ready
        room_players = db_handler.get_room_players(room_uid)
        player_uid = None
        for player in room_players:
            if str(player.username) == str(request.user):
                player_uid = player.player_uid
                break

        if player_uid is None:
            return redirect('/')

        for i in range(5):
            for p in room_players:
                utils.deal_card(room_uid, p.player_uid,
                                db_handler.DBClassPOINT(0, 0))

        context = load_play_info(room_uid, player_uid)



        return render(request, 'play.html', context=context)
