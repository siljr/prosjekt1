from django.conf.urls import url
from . import views


app_name = "bandmedlem"
urlpatterns = [
    url(r'^view_bandmedlem$', views.BookingListView.as_view(), name='bookings')
]