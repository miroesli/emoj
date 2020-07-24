from django.http import HttpResponse
from project import utils
import json
import ast


def id(request, id): 
    return HttpResponse("You're looking at id %s." % id)

<<<<<<< HEAD

# def get_user_id(request, user):
#     id = user.
#     return HttpResponse(id)


def option(request, data):
    # if request.method == get (separate functions to check which button options are avaialbe and return with that list.)

    # else if request.method == post (send the json to the utils function_handler)

    return utils.function_handler(request.body)
# TODO: add/modify a function to call utils with all the backend passing.
# include the necessary data as a json payload?
# Should be in the request.body?
# https://stackoverflow.com/questions/45072255/axios-post-array-data
# possibly have the different functions return different HttpResponse.status_code HttpReponse.content depending on it's error handling
=======
def option(request):

    # An action has been submitted and needs to be processed.
    if(request.method == 'POST'): 
        dict_str = request.body.decode('utf8')
        data = ast.literal_eval(dict_str)
        import pdb; pdb.set_trace()
        return utils.function_handler(data)

    # An item has been selected and the possible options need to be displayed.
    elif(request.method == 'GET'):
        # TODO: double check axios get request parameter accessing
        dict_str = request.body.decode('utf8')
        data = ast.literal_eval(dict_str)
        import pdb; pdb.set_trace()
        return utils.display_options(data)
>>>>>>> 1882dd447e86d4206e2b3d2fd8f288d96b5924c4
