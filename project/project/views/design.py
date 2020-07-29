from django.shortcuts import render
from project import db_handler
import json


def stringy(o):
    return o.__str__()


def render_design(request):
    cards = db_handler.get_cards()
    templates = db_handler.get_all_templates()
    context = {"cards": [i.to_dict() for i in cards], 'templates': [i.to_dict() for i in templates]}
    return render(request, 'design.html', context=context)
