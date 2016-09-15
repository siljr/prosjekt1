from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.login_page, name='login'),
    url(r'^logout$', views.login_page, name='logout'),
    url(r'^auth$', views.login_authenticate, name='login_auth')
]
