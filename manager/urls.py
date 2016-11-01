from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from . import views

app_name = "manager"

urlpatterns = [
    url(r'^technical_needs/$', views.changeTechnicalneed, name='changeNeeds'),
    url(r'^technical/requirements/$', permission_required('band_booking.see_technical_requirements', login_url="/login")(views.technical_requirements), name='technical_requirements'),
    url(r'^technical/requirements/update/$', permission_required('band_booking.see_technical_requirements', login_url="/login")(views.update_technical_requirements), name='technical_requirements_update'),
]
