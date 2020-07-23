from django.http import HttpResponse
import utils.py


def id(request, id):
    return HttpResponse("You're looking at id %s." % id)

def option(request, data):
    return utils.function_handler(request.body)
# TODO: add/modify a function to call utils with all the backend passing.
# include the necessary data as a json payload?
# Should be in the request.body?
# https://stackoverflow.com/questions/45072255/axios-post-array-data
# possibly have the different functions return different HttpResponse.status_code HttpReponse.content depending on it's error handling