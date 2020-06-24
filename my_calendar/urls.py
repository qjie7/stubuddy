from django.contrib import admin
from django.urls import include, path

from .views import *

app_name = 'my_calendar'

urlpatterns = [
    path('', add_event, name='add_event'),
    path('view', calendar, name='view'),
    path('success', success, name='success')
]
