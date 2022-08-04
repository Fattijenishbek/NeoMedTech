from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import (
    LoginMobileSerializer,
    LoginWebSerializer,
    RegisterSerializer,
    RegisterPatientSerializer,
    UserSerializer, DoctorProfileSerializer,
    PatientProfileSerializer,
    # PasswordResetConfirmSerializer, PasswordResetSerializer,
)

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterPatientView(generics.GenericAPIView):
    serializer_class = RegisterPatientSerializer

    def post(self, request):
        serializer = RegisterPatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginWebView(generics.GenericAPIView):
    serializer_class = LoginWebSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data['email']
        password = request.data["password"]

        user = User.objects.get(email=email)
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        refresh = RefreshToken.for_user(user)

        is_superuser = user.is_superuser
        user_type = user.user_type
        id = user.id
        return Response(
            {
                'user_id': id,
                "status": "You successfully logged in",
                "is_superuser": is_superuser,
                "user_type": user_type,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class LoginMobileView(generics.GenericAPIView):
    serializer_class = LoginMobileSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        phone = request.data['phone']

        user = User.objects.filter(phone=phone).first()
        if user is None:
            raise AuthenticationFailed("User not found!")

        refresh = RefreshToken.for_user(user)

        is_superuser = user.is_superuser
        user_type = user.user_type
        id = user.id
        return Response(
            {
                'user_id': id,
                "status": "You successfully logged in",
                "is_superuser": is_superuser,
                "user_type": user_type,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class OfficeManagerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='office_manager')
    serializer_class = UserSerializer


class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='doctor')
    serializer_class = DoctorProfileSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='patient')
    serializer_class = PatientProfileSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'first_name',
                       'last_name', 'address',
                       'phone', 'birth_date',
                       'age',
                       'patient__id', 'patient__date_of_pregnancy',
                       'patient__inn', 'patient__doctor']
