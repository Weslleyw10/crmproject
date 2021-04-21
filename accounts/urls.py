from django import urls
from django.contrib import auth
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.products, name='products'),
    path('customer/<str:pk>', views.customers, name='customer'),

    path('createOrder/<str:pk>', views.createOrder, name='createOrder'),
    path('updateOrder/<str:pk>', views.updateOrder, name='updateOrder'),
    path('deleteOrder/<str:pk>', views.deleteOrder, name='deleteOrder'),

    path('register', views.register, name='register'),
    path('login', views.loginSystem, name='login'),
    path('logout', views.logoutSystem, name='logout'),
    path('profile', views.profile, name='user-page'),
    path('account', views.account, name='account'),

    path('password/reset', 
    auth_views.PasswordResetView.as_view(template_name="emails/password_reset.html"),
    name='reset_password'),

    path('password/sent',
    auth_views.PasswordResetDoneView.as_view(template_name="emails/password_sent.html"),
    name='password_reset_done'),

    path('password/reset/<uidb64>/<token>',
    auth_views.PasswordResetConfirmView.as_view(template_name="emails/password_reset_form.html"),
    name='password_reset_confirm'),

    path('password/complete',
    auth_views.PasswordResetCompleteView.as_view(template_name="emails/password_complete.html"),
    name='password_reset_complete'),


]