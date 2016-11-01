from django.conf.urls import url
from . import views


app_name = "bandmedlem"
urlpatterns = [
    url(r'^band/calendar/(?P<year>([0-9]{4}))/(?P<month>(([1][0-2]|[1-9]{1})))/$', views.concerts_band, name='calendar')
]