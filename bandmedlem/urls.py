from django.conf.urls import url
from . import views


app_name = "bandmedlem"
urlpatterns = [
    url(r'^offers/band/$', views.BandListView.as_view(), name='bookings')
]
