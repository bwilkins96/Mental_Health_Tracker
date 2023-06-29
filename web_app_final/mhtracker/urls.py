from django.urls import path
from . import views

app_name = 'mhtracker'
urlpatterns = [
    path('', views.index, name='index'),
    path('logs/', views.MentalLogListView.as_view(), name='list'),
    path('logs/create/', views.MentalLogCreate.as_view(), name='create'),
    path('logs/<int:pk>/delete/', views.MentalLogDelete.as_view(), name='delete'),
    path('logs/<int:pk>/', views.MentalLogUpdate.as_view(), name='edit')
]
