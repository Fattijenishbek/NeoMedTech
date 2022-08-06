from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OfficeManager, Patient, Doctor, User
from .api.serializers import AdminSerializer, OfficeManagerSerializer, \
    PatientSerializer, DoctorSerializer, DoctorListSerializer, PatientListSerializer
from .api.login_serializers import DoctorLoginWebSerializer, PatientLoginMobileSerializer, OfficeManagerLoginSerializer
from .api.register_serializer import RegisterOfficeManagerSerializer, RegisterPatientSerializer, \
    RegisterDoctorSerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class RegisterOfficeManagerView(generics.CreateAPIView):
    serializer_class = RegisterOfficeManagerSerializer
    queryset = OfficeManager.objects.all()


class RegisterPatientView(generics.CreateAPIView):
    serializer_class = RegisterPatientSerializer
    queryset = Patient.objects.all()


class RegisterDoctorView(generics.CreateAPIView):
    serializer_class = RegisterDoctorSerializer
    queryset = Doctor.objects.all()


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


class LoginMobileView(generics.GenericAPIView):
    serializer_class = PatientLoginMobileSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        phone = request.data['phone']

        user = Patient.objects.filter(phone=phone).first()
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
