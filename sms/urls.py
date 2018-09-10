from django.conf.urls import re_path
from django.urls import path

from . import views

urlpatterns = [
    path('', views.sms_response, name='sms'),
    path('contest/', views.select_and_notify, name='contest')
]