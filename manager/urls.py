from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from . import views

app_name = "manager"

urlpatterns = [
    url(r'^technical_needs/$', views.changeTechnicalneed, name='changeNeeds'),
]
