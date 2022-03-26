from django.urls import path
from acc_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login-view'),
    path('login/verify-otp/', views.verify_otp, name='verify-otp'),
    path('resend-otp/', views.resend_otp, name='resend-otp'),
    path('logout/', views.logout_user, name='logout-view'),
    path('signup/', views.signup_view, name='signup-view'),
    path('signup-confirm/', views.signup_confirm, name='signup-confirm'),
    path('verify-user/<uidb64>/<token>/', views.verify_user, name='verify-user'),
]
