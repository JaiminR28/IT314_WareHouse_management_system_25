from django.urls import path, re_path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('', views.index, name='default'),    
    path('login', views.login, name='login'),
    path('login/validate', views.loginValidate, name='loginValidate'),
    path('register', views.register, name='register'),
    path('register/entry', views.registerEntry, name='registerEntry'),
    path('index', views.index, name='index'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('logout', views.logout, name='logout'),
    path('report', views.report, name='report'),
    path('generatePDF', views.generatePDF, name='generatePDF'),
    path('mailPDF', views.mailPDF, name='mailPDF'),
    path('videoCall', views.videoCall, name='videoCall'),
    path('show-reservations', views.showReservations, name='showReservations'),
    path('add-item', views.addItem, name='addItem'),
    path('add-item/entry', views.itemEntry, name='itemEntry'),
    path('performVideoCall', views.performVideoCall, name='performVideoCall'),
    re_path(r'^modify-reservation/(?P<reservation_id>[-\w\d]+)$', views.modifyReservation, name='modifyReservation'),
    re_path(r'^modify-reservation/entry/(?P<reservation_id>[-\w\d]+)$', views.modifyReservationEntry, name='modifyReservationEntry'),
]