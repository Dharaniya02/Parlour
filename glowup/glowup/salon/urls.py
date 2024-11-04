# salon/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import  notifications_view
from . import views
from .views import (
    #user_dashboard,
    #appointments_view,
    booking_history,
    profile_view,
    notifications_view,
    support_view,
    
    # other views...
)

urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),  # User login
    path('admin_login/', views.admin_login, name='admin_login'),  # Admin login
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),  # User dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'), 
    
    path('about/', views.about, name='about'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),
    path('services/facial/', views.facial, name='facial'),
    path('services/haircut/', views.haircut, name='haircut'),
    path('services/massage/', views.massage, name='massage'),
    path('services/manicure_pedicure/', views.manicure_pedicure, name='manicure_pedicure'),
    path('services/bridal_makeup/', views.bridal_makeup, name='bridal_makeup'),
    path('services/waxing/', views.waxing, name='waxing'),
    path('services/', views.services, name='services'),
    path('profile/', views.profile_view, name='profile'),
    path('booking-history/', booking_history, name='booking_history'),  # Booking history page
    path('user_dasboard/profile/', profile_view, name='profile_view'),  # Profile settings page
    path('notifications/', notifications_view, name='notifications'),  # Notifications page
    path('support/', support_view, name='support'),  # Support page
    path('booking-history/', views.booking_history, name='booking_history'),
     path('exclusive-offers/', views.exclusive_offers_view, name='exclusive_offers'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('admin/manage_offers/', views.manage_offers, name='manage_offers'),
    path('admin/system_settings/', views.system_settings, name='system_settings'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('manage_appointments/', views.manage_appointments, name='manage_appointments'),
    path('accept_appointment/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('offers/', views.offer_list, name='offer_list'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('manage_users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('manage_users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('get_dashboard_counts/', views.get_dashboard_counts, name='get_dashboard_counts'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)