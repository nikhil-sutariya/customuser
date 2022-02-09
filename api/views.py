from rest_framework import generics
from .serializer import UserSerializer
from acc_app.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

class UserList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

