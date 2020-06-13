from django.http import HttpResponse


def id(request, id):
    return HttpResponse("You're looking at id %s." % id)
