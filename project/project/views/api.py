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
        # TODO: double check axios get request parameter accessing
        dict_str = request.body.decode('utf8')
        data = ast.literal_eval(dict_str)
        import pdb
        pdb.set_trace()
        return utils.display_options(data)
