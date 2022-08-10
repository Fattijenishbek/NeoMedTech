from datetime import datetime, timedelta
import datetime as agahan
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# from checklist.models import CheckList
from .models import OfficeManager, Patient, Doctor, User
from .api.serializers import (
    AdminSerializer,
    OfficeManagerSerializer,
    PatientSerializer,
    DoctorSerializer,
    DoctorListSerializer,
    PatientListSerializer,
)
from .api.password_reset_serializers import (
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)
from .api.login_serializers import (
    DoctorLoginWebSerializer,
    PatientLoginMobileSerializer,
    OfficeManagerLoginSerializer,
)
from .api.register_serializer import (
    RegisterOfficeManagerSerializer,
    RegisterPatientSerializer,
    RegisterDoctorSerializer,
)
from .permissions import (
    IsSuperUser,
    IsSuperUserOrOfficeManager,
    IsSuperUserOrOfficeManagerOrDoctor,
)

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class RegisterOfficeManagerView(generics.CreateAPIView):
    serializer_class = RegisterOfficeManagerSerializer
    queryset = OfficeManager.objects.all()
    permission_classes = (IsSuperUser,)


class RegisterPatientView(generics.CreateAPIView):
    serializer_class = RegisterPatientSerializer
    queryset = Patient.objects.all()
    permission_classes = (IsSuperUserOrOfficeManagerOrDoctor, )

    # def create(self, request, *args, **kwargs):
    #     serializer = RegisterPatientSerializer(data=request.data)
    #     patient = request.data['patient']
    #     doctor = request.data['doctor']
    #     if serializer.is_valid():
    #         serializer.save()
    #         # for i in range(1, 10):
    #         #     CheckList.objects.get_or_create(patient=patient, doctor=doctor, month=i)
    #
    #         return Response(status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterDoctorView(generics.CreateAPIView):
    serializer_class = RegisterDoctorSerializer
    queryset = Doctor.objects.all()
    permission_classes = (IsSuperUserOrOfficeManager, )


class DoctorLoginWebView(generics.GenericAPIView):
    serializer_class = DoctorLoginWebSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data['email']
        password = request.data["password"]

        user = Doctor.objects.get(email=email)
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


class OfficeManagerLoginView(generics.GenericAPIView):
    serializer_class = OfficeManagerLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data['email']
        password = request.data["password"]

        user = OfficeManager.objects.get(email=email)
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
    serializer_class = PatientLoginMobileSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        phone = request.data['phone']

        user = Patient.objects.filter(phone=phone).first()
        if user is None:
            raise AuthenticationFailed("User not found!")

        refresh = RefreshToken.for_user(user)
        id = user.id
        is_superuser = user.is_superuser
        user_type = user.user_type
        expires_in = refresh.access_token.lifetime.total_seconds()
        expires_day = agahan.datetime.now() + timedelta(seconds=expires_in)
        return Response(
            {
                'user_id': id,
                "status": "You successfully logged in",
                "expires_day": expires_day,
                "is_superuser": is_superuser,
                "user_type": user_type,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class OfficeManagerViewSet(viewsets.ModelViewSet):
    queryset = OfficeManager.objects.all()
    serializer_class = OfficeManagerSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorSerializer
        return DoctorListSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientSerializer
        return PatientListSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=True)
    serializer_class = AdminSerializer
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
