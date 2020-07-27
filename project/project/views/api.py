from django.http import HttpResponse
from project import utils, db_handler
import json
import ast
import uuid


def id(request, id):
    return HttpResponse("You're looking at id %s." % id)


def option(request):
    # An action has been submitted and needs to be processed.
    if(request.method == 'POST'):
        data = json.loads(request.body)
        room_uid = data.get('room_uid')
        player_uid = data.get('player_uid')
        option = data.get('option')
        selected = data.get('selected')
        return HttpResponse(json.dumps(utils.function_handler(room_uid, player_uid, option, selected)))

    # An item has been selected and the possible options need to be displayed.
    elif(request.method == 'GET'):
        room_uid = request.GET.get('room_uid')
        player_uid = request.GET.get('player_uid')
        selected = json.loads(request.GET.get('selected'))
        return HttpResponse(json.dumps(utils.display_options(room_uid, player_uid, selected)))


def open_room(request):
    print('open room')
    print(request.body)
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        room_name = data.get('room_name')
        positions = data.get('positions')
        template_name = data.get('template_name')
        template_uid = data.get('template_uid')

        if template_uid in [None, ""]:
            template_uid = uuid.uuid4()
            db_handler.create_new_template( template_name, template_uid)

            first_deck_uid = db_handler.get_first_deck().deck_uid
            print(first_deck_uid)
            db_handler.insert_template_deck(template_uid, first_deck_uid, 0, 0)

            for p in positions:
                x = int(p[0])
                y = int(p[1])
                db_handler.insert_template_deck(template_uid, None, x, y)

    #     TODO: create a new template uid
    #  create template, load deck
    # link template to room
    # first deck from decks for position 00
    # other decks are null

    return HttpResponse(json.dumps('test'))
