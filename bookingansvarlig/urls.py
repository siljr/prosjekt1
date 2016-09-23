from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from . import views

__author__ = 'Weronika'

urlpatterns = [
    url(r'^scenes$',
        permission_required('band_booking.view_scenes', login_url='/login')(views.ScenesListView.as_view()),
        name='scenes')
]
