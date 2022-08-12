from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from checklist.models import (
    CheckList,
    CheckListTemplate,
    Answer,
)
from checklist.serializers import CheckListTemplateListSerializer
from .models import OfficeManager, Patient, Doctor, User

from .api.serializers import (
    AdminSerializer,
    OfficeManagerSerializer,
    PatientSerializer,
    DoctorSerializer,
    DoctorListSerializer,
    PatientListSerializer,
)
from .api.login_serializers import (
    PersonalLoginWebSerializer,
    PatientLoginMobileSerializer,
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
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUser,)


class RegisterPatientView(generics.CreateAPIView):
    serializer_class = RegisterPatientSerializer
    queryset = Patient.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManagerOrDoctor,)

    def create(self, request, *args, **kwargs):
        serializer = RegisterPatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            doctor = request.data['doctor_field']
            patient = Patient.objects.latest('id').id if Patient.objects.exists() else 1
            template = CheckListTemplate.objects.latest('id')
            answer_data = CheckListTemplateListSerializer(template).data
            answers = []
            for i in answer_data['title']:
                for j in i['question']:
                    answers.append(j['id'])
            for month in range(1, 10):
                a = CheckList.objects.create(month=month, doctor_id=doctor, patient_id=patient, template=template)
                for question_id in answers:
                    Answer.objects.create(question_id=question_id, check_list=a)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterDoctorView(generics.CreateAPIView):
    serializer_class = RegisterDoctorSerializer
    queryset = Doctor.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManager,)


class PersonalLoginWebView(generics.GenericAPIView):
    serializer_class = PersonalLoginWebSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data['email']
        password = request.data["password"]
        if Doctor.objects.filter(email=email).exists():
            user = Doctor.objects.get(email=email)
        elif OfficeManager.objects.filter(email=email).exists():
            user = OfficeManager.objects.get(email=email)
        else:
            user = User.objects.get(email=email)

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        refresh = RefreshToken.for_user(user)

        is_superuser = user.is_superuser
        user_type = user.user_type
        id = user.id
        expires_in = refresh.access_token.lifetime.total_seconds()
        expires_day = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        return Response(
            {
                'user_id': id,
                "status": "You successfully logged in",
                "is_superuser": is_superuser,
                "expires_day": expires_day,
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
        expires_day = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
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
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManager,)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManager,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return DoctorSerializer
        return DoctorListSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManager,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PatientSerializer
        return PatientListSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=True)
    serializer_class = AdminSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManager,)
