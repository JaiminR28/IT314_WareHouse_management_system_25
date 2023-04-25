from django.urls import path, re_path
from . import views

app_name = 'farmer'

urlpatterns = [
    path('', views.index, name='default'),
    path('login', views.login, name='login'),
    path('login/validate', views.loginValidate, name='loginValidate'),
    path('register', views.register, name='register'),
    path('register/entry', views.registerEntry, name='registerEntry'),
    path('logout', views.logout, name='logout'),
    # path('storedGoods', views.storedGoods, name='storedGoods'),
    path('home', views.home, name='home'),
    path('index', views.index, name='index'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('search-nearby-warehouses', views.searchNearbyWarehouses, name='searchNearbyWarehouses'),
    path('show-nearby-warehouses', views.showNearbyWarehouses, name='showNearbyWarehouses'),
    path('make-reservation', views.makeReservation, name='makeReservation'),
    path('make-reservation/entry', views.reservationEntry, name='reservationEntry'),
    path('show-reservations', views.showReservations, name='showReservations'),
    path('add-item', views.addItem, name='addItem'),
    path('add-item/entry', views.itemEntry, name='itemEntry'),
    re_path(r'^modify-reservation/(?P<reservation_id>[-\w\d]+)$', views.modifyReservation, name='modifyReservation'),
    re_path(r'^modify-reservation/entry/(?P<reservation_id>[-\w\d]+)$', views.modifyReservationEntry, name='modifyReservationEntry'),
    path('show-crop-suggestions', views.showCropSuggestions, name='showCropSuggestions'),
    path('videoCall', views.videoCall, name='videoCall'),
    path('generateReport', views.generateReport, name='generateReport'),
    re_path(r'^delete-reservation/(?P<reservation_id>[-\w\d]+)$', views.deleteReservation, name='deleteReservation'),
]