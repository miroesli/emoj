from django.shortcuts import render
from project import db_handler
import json


def stringy(o):
    return o.__str__()


def render_design(request):
    cards = db_handler.get_cards()
    context = {"cards":[json.dumps(i.to_dict(), default = stringy) for i in cards]}
    return render(request, 'design.html', context = context)