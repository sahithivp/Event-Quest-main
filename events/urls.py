from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('book-hall/', views.hall_booking, name='book_hall'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('submit_appointment/', views.submit_appointment, name='submit_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('view_profile/', views.view_profile, name='view_profile'),
]
