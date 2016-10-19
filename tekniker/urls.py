from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from . import views

app_name = "tekniker"

urlpatterns = [
    url(r'^myconcerts/$', views.tekniker_concerts, name="myconcerts")
]