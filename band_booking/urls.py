from django.conf.urls import url

from . import views

app_name = 'band_booking'
urlpatterns = [
    url(r'^login(?P<error>(/error))?$', views.login_page, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^auth$', views.login_authenticate, name='login_auth'),
    url(r'^artist/(?P<name>([A-Za-z0-9 ]+))$', views.artist_load, name='artist_load'),
    url(r'^get_artist/(?P<name>([A-Za-z0-9 ]+))$', views.artist, name='artist'),
    url(r'^event_information/(?P<name>([A-Za-z0-9 ]+))$', views.event_load, name='past_events'),
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
]
