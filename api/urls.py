from django.urls import path, include
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('register', views.RegisterView.as_view(), name = 'userlist'),
    path('user/<int:pk>/', views.UserDetails.as_view(), name = 'user'),
]
