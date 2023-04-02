from django.urls import path
from . import views

app_name = 'farmer'

urlpatterns = [
    path('', views.login, name='default'),
    path('login', views.login, name='login'),
    path('login/validate', views.loginValidate, name='loginValidate'),
    path('register', views.register, name='register'),
    path('register/entry', views.registerEntry, name='registerEntry'),
    path('home', views.home, name='home'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]