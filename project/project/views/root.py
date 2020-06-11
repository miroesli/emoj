from django.http import HttpResponseRedirect


def render_root(request):
    return HttpResponseRedirect("home/")
