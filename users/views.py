from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django_filters import rest_framework as filters
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import AuthenticationFailed
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
    PatientProfileSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer
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
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ('first_name', 'birth_date')
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


class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.
    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"success": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": ("Password has been reset with the new password.")}
        )
