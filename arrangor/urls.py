from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from . import views

__author__ = 'Weronika'


urlpatterns = [
    url(r'^concerts_in_semester/$', views.ConcertsView.as_view(), name='concerts'),
]