from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reserve/<str:pk>/', views.reserve, name='reserve'),
    path('user_reserves/', views.user_reserves, name='user_reserves'),
    path('rules/', views.rules, name='rules'),
    path('api/', views.api, name='api'),
    path('api/events', views.api_events_list, name='api_events_list'),
    path('api/event/<str:pk>/', views.api_single_event, name='api_single_event'),
]