from django.shortcuts import render
from project import db_handler



def render_home(request):
    rooms = db_handler.get_rooms()
    r = [{'room_uid': y, 'room_name': x} for x, y in rooms]
    context = {'rooms': r}
    return render(request, 'home.html', context)
