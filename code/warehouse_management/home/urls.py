from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('sendQuery/', views.sendQuery, name='sendQuery'),
]
