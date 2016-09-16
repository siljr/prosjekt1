from django.conf.urls import url

from . import views


__author__ = 'Weronika'


urlpatterns = [
    url(r'^scenes$', views.ScenesListView.as_view(), name='scenes')
]
