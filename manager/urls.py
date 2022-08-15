
from django.urls import path
from django import views
from . import views
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('',Application.as_view(),name='dashboard'),
    path('stats',views.stats,name='stats'),
    path('accounts/login',UserAuth.as_view(),name='manager dashboard'),
    path('accounts/logout/',views.user_logout,name='logout'),
    path('accounts/reset_password/',auth_views.PasswordResetView.as_view(form_class=UserResetPassword,template_name='manager/password_reset.html'),name='reset_password'),
    path('accounts/reset_password_done/',auth_views.PasswordResetDoneView.as_view(template_name='manager/password_reset_done.html'),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='manager/password_reset_confirm.html'),name='password_reset_confirm'),
    path('accounts/reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='manager/password_reset_complete.html'),name='password_reset_complete'),
]