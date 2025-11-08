from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),
    path('menu/', views.menu, name='menu'),
    path('menu_item/<int:pk>/', views.menu_item, name='menu_item'),
    path('bookings/', views.bookings, name='bookings'),
    path('api/bookings/', views.bookings, name='api_bookings'),
    path('api/submit_booking/', views.submit_booking, name='submit_booking'),
    path('api/available_slots/', views.available_slots, name='available_slots'),
]