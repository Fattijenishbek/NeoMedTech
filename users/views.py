from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import (
    LoginSerializer,
    RegisterSerializer,

)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        phone = request.data["phone"]
        password = request.data["password"]
        print(password)
        user = User.objects.get(phone=phone)
        if user is None:
            raise AuthenticationFailed("User not found!")

        if password != user.password:
            raise AuthenticationFailed("Incorrect password!")

        refresh = RefreshToken.for_user(user)

        is_superuser = user.is_superuser
        user_type = user.user_type

        return Response(
            {
                "status": "You successfully logged in",
                "is_superuser": is_superuser,
                "user_type": user_type,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )