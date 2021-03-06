"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.urls import re_path, path, include
from django.contrib import admin
from project.views import root, api, home, design, play
# from django.views.generic.base import TemplateView

urlpatterns = [
    path('', root.render_root, name='root'),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('api/<int:id>', api.id),
    path('api/options', api.option),
    path('api/open_room', api.open_room),
    path('api/load_play', api.load_play),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', home.render_home, name='home'),
    re_path(r'^play/(?P<room_uid>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})', play.render_play, name='play'),
    path('play/',play.render_play),
    path('design/', design.render_design),
]
