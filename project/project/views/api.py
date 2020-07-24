from django.http import HttpResponse
from project import utils
import json
import ast


def id(request, id):
    return HttpResponse("You're looking at id %s." % id)


def option(request):
    # An action has been submitted and needs to be processed.
    if(request.method == 'POST'):
        dict_str = request.body.decode('utf8')
        data = ast.literal_eval(dict_str)
        import pdb
        pdb.set_trace()
        return utils.function_handler(data)

    # An item has been selected and the possible options need to be displayed.
    elif(request.method == 'GET'):
        room_uid = request.GET.get('room_uid')
        player_uid = request.GET.get('player_uid')
        selected = json.loads(request.GET.get('selected'))
        return json.dumps(utils.display_options(room_uid, player_uid, selected))
