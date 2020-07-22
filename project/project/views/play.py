from django.shortcuts import render
from project import db_handler

# example of uid CA761232-ED42-11CE-BACD-00AA0057B223
def render_play(request, room_uid):
    room_players = db_handler.get_players() # replace with get room players when data is ready
    # we will need to get a specific player via cookies eventually but for now I set the first player as active
    player = room_players[0]
    room_players = room_players[1:]
    player.hand = [i.to_dict() for i in db_handler.get_player_cards(player.player_uid, room_uid)]
    for p in room_players:
        p.hand = db_handler.get_player_card_revealed(p.player_uid, room_uid)
        p.card_count = db_handler.get_player_card_count(p.player_uid, room_uid)


    context = {"player": player.to_dict(),"players": [i.to_dict() for i in room_players]}
    return render(request, 'play.html', context=context)
