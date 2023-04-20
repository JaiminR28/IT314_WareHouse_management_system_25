from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('', views.index, name='default'), 
    path('generateReport', views.generateReport, name='generateReport'),   
    path('login', views.login, name='login'),
    path('login/validate', views.loginValidate, name='loginValidate'),
    path('register', views.register, name='register'),
    path('register/entry', views.registerEntry, name='registerEntry'),
    path('index', views.index, name='index'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('logout', views.logout, name='logout'),
    path('report', views.report, name='report'),
    path('generatePDF', views.generatePDF, name='generatePDF'),
]