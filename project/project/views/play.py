from django.shortcuts import render
from project import db_handler, utils
from django.contrib.auth.models import Permission, User


def load_play_info(room_uid):
    pass


# example of uid 36e37bb4-cc52-11ea-b508-784f437b7506
def render_play(request, room_uid):
    room = db_handler.get_room(room_uid)
    if not room:
        pass  # add error handling
    else:
        utils.reset_room(room_uid)
        # replace with get room players when data is ready
        room_players = db_handler.get_players()
        # we will need to get a specific player via cookies eventually but for now I set the first player as active

        # utils.deal_card(room_uid, p.player_uid, '(0,0)')
        # # TODO HERE
        # print(request.user)
        # print(request.COOKIES)
        # player_index = 0
        # player = room_players[player_index]  # base this from session info
        # # this will also have to change with above excluding the current player
        # # room_players = []

        # # for i in range(room_players):
        # #     if i != player_index:
        # #         room_players.append(room_players[i])
        # room_players[1:]
        # print(room_players[0].username)

        # player.hand = [i.to_dict() for i in db_handler.get_player_cards(
        #     player.player_uid, room_uid)]

        for i in range(5):
            for p in room_players:
                utils.deal_card(room_uid, p.player_uid,
                                db_handler.DBClassPOINT(0, 0))
        player = room_players[0]  # base this from session info
        # this will also have to change with above excluding the current player
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
