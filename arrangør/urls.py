from django.conf.urls import url
from . import views


app_name = "arrangør"
urlpatterns = [
     url(r'^concerts_in_semester/$', views.ConcertsView.as_view(), name='concerts'),
]