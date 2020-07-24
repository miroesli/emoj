from django.shortcuts import render
from project import db_handler, utils


# example of uid 36e37bb4-cc52-11ea-b508-784f437b7506
def render_play(request, room_uid):
    room = db_handler.get_room(room_uid)
    if not room:
        pass# add error handling
    else:
        utils.reset_room(room_uid)
        room_players = db_handler.get_players() # replace with get room players when data is ready
        # we will need to get a specific player via cookies eventually but for now I set the first player as active
        for i in range(5):
            for p in room_players:
                utils.deal_card(room_uid, p.player_uid, '(0,0)')
        player = room_players[0] # base this from session info
        room_players = room_players[1:] #this will also have to change with above excluding the current player
        player.hand = [i.to_dict() for i in db_handler.get_player_cards(player.player_uid, room_uid)]
        for p in room_players:
            p.hand = db_handler.get_player_card_revealed(p.player_uid, room_uid)
            p.card_count = db_handler.get_player_card_count(p.player_uid, room_uid)

        # TODO: add more details to the context, everything we possibly need in play.
        # Possibly do a similar with the room_players in merging all the game template/deck information into one object
        context = {"player": player.to_dict(),"players": [i.to_dict() for i in room_players],"room": room}
        return render(request, 'play.html', context=context)
