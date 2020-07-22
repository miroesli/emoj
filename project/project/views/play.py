from django.shortcuts import render
from project import db_handler

# example of uid CA761232-ED42-11CE-BACD-00AA0057B223
def render_play(request, room_uid):
    room_players = db_handler.get_players() # replace with get room players when data is ready
    # we will need to get a specific player via cookies eventually but for now I set the first player as active
    player = room_players[0]
    for p in room_players:
        if p.player_uid != player.player_uid:
            p.hand = db_handler.get_player_card_revealed(p.player_uid, room_uid)
            p.card_count = db_handler.get_player_card_count(p.player_uid, room_uid)
        else:
            player.hand = [i.to_dict() for i in db_handler.get_player_cards(player.player_uid, room_uid)]

    context = {"players": [i.to_dict() for i in room_players]}
    return render(request, 'play.html', context=context)
