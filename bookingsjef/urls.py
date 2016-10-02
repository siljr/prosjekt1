from django.conf.urls import url

from . import views


app_name = "bookingsjef"
urlpatterns = [
    url(r'^economy/concert/(?P<id>([0-9]+))/$', views.economic_result_concert, name="economic_result")
]
