from django.shortcuts import render


# example of uid CA761232-ED42-11CE-BACD-00AA0057B223
def render_play(request, uid):
    return render(request, 'play.html')
