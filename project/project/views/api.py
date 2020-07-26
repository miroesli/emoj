from django.http import HttpResponse
from project import utils
import json
import ast


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
