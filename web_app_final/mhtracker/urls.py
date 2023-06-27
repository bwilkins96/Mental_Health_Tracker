from django.urls import path
from . import views

app_name = 'mhtracker'
urlpatterns = [
    path('', views.index, name='index')
]
