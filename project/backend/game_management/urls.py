# game_management/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('game/<int:game_id>/move/', views.make_move, name='make_move'),
    # Add other URL patterns here
]