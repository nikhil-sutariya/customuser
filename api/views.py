from calendar import c
from rest_framework import generics, status
from .serializer import UserSerializer, LogoutSerializer
from acc_app.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class RegisterView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated, )

#     def post(self, request):
#         try:
#             refresh_token = request.get["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status = status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status = status.HTTP_400_BAD_REQUEST)
class LogoutView(generics.GenericAPIView):
    serializer = LogoutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(status.HTTP_204_NO_CONTENT)
            
