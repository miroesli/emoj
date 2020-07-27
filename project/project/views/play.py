from django.shortcuts import render, redirect
from project import db_handler, utils
from django.contrib.auth.models import Permission, User
from collections import deque


def load_play_info(room_uid):
    pass


# example of uid 36e37bb4-cc52-11ea-b508-784f437b7506
def render_play(request, room_uid):
    room = db_handler.get_room(room_uid)
    if not room:
        return redirect('/')
    else:
        utils.reset_room(room_uid)
        # replace with get room players when data is ready
        room_players = db_handler.get_players()

        player_index = None
        for index, player in enumerate(room_players):
            if str(player.username) == str(request.user):
                player_index = index
                break

        if player_index is None:
            return redirect('/')

        for i in range(5):
            for p in room_players:
                utils.deal_card(room_uid, p.player_uid,
                                db_handler.DBClassPOINT(0, 0))

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

        # TODO: add more details to the context, everything we possibly need in play.
        # Possibly do a similar with the room_players in merging all the game template/deck information into one object

        context = {"player": player.to_dict(), "players": [
            i.to_dict() for i in room_players], "room": room}
        return render(request, 'play.html', context=context)
