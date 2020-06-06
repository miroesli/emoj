from django.shortcuts import render
from project import db_handler
import json


def stringy(o):
    return o.__str__()


def render_design(request):
    cards = db_handler.get_cards()
    context = {"cards": [i.to_dict() for i in cards]}
    return render(request, 'design.html', context = context)