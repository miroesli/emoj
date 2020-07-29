from django.shortcuts import render, redirect
from project import db_handler, utils
from django.contrib.auth.models import Permission, User
from collections import deque





# example of uid 36e37bb4-cc52-11ea-b508-784f437b7506
def render_play(request, room_uid):
    room = db_handler.get_room(room_uid)
    if not room:
        return redirect('/')
    else:
        utils.reset_room(room_uid)
        # replace with get room players when data is ready
        players = db_handler.get_players()
        player_uid = None
        for player in players:
            if str(player.username) == str(request.user):
                player_uid = player.player_uid
                break
        if player_uid is None:
            return redirect('/')

        context = utils.load_play_info(room_uid, player_uid)
        return render(request, 'play.html', context=context)
