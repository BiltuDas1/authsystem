from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.login),
  path('register/', views.register),
  path('logout/', views.logout),
  path('email/verify/', views.verify_email),
  path('email/reset-password/', views.reset_password),
  path('email/reset-password/verifyToken', views.check_reset_token),
  path('email/reset-password/change', views.change_password)
]