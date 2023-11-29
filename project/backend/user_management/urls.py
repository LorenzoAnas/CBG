from django.url import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
]
