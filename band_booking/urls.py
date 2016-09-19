from django.conf.urls import url

from . import views

app_name = 'band_booking'
urlpatterns = [
    url(r'^login(?P<error>(/error))?$', views.login_page, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^auth$', views.login_authenticate, name='login_auth')
]