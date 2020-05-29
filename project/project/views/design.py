from django.shortcuts import render


def render_design(request):
    return render(request, 'design.html')