import xlwt
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from checklist.models import (
    CheckList,
    CheckListTemplate,
    Answer, MedCard,
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
    RegisterAdminSerializer
)
from .permissions import (
    IsSuperUser,
    IsSuperUserOrOfficeManager,
    IsSuperUserOrOfficeManagerOrDoctor,
)
from .api.custom_funcs import get_token

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class RegisterAdminView(generics.CreateAPIView):
    serializer_class = RegisterAdminSerializer
    queryset = User.objects.all()

class RegisterOfficeManagerView(generics.CreateAPIView):
    serializer_class = RegisterOfficeManagerSerializer
    queryset = OfficeManager.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUser,)


class RegisterPatientView(generics.CreateAPIView):
    serializer_class = RegisterPatientSerializer
    queryset = Patient.objects.all()

    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManagerOrDoctor,)

    def create(self, request, *args, **kwargs):
        serializer = RegisterPatientSerializer(data=request.data)
        if serializer.is_valid():
            if not CheckListTemplate.objects.exists():
                return Response('You must create CheckListTemplate before Patient', status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            patient = Patient.objects.latest('id').id if Patient.objects.exists() else 1
            template = CheckListTemplate.objects.latest('id')
            answer_data = CheckListTemplateListSerializer(template).data
            answers = []
            for i in answer_data['title']:
                for j in i['question']:
                    answers.append(j['id'])
            for month in range(1, 10):
                a = CheckList.objects.create(month=month, patient_id=patient, template=template)
                for question_id in answers:
                    Answer.objects.create(question_id=question_id, check_list=a)
            MedCard.objects.create(patient_id=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterDoctorView(generics.CreateAPIView):
    serializer_class = RegisterDoctorSerializer
    queryset = Doctor.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)


class PersonalLoginWebView(generics.GenericAPIView):
    serializer_class = PersonalLoginWebSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data['email']
        password = request.data["password"]
        user = User.objects.filter(email=email).first()
        if user is None or User.objects.filter(email=email, is_active=False):
            raise AuthenticationFailed("User not found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        return get_token(user)


class LoginMobileView(generics.GenericAPIView):
    serializer_class = PatientLoginMobileSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        phone = request.data['phone']
        user = Patient.objects.filter(phone=phone).first()
        if user is None or not user.is_active:
            raise AuthenticationFailed("User not found!")
        return get_token(user)


class OfficeManagerViewSet(viewsets.ModelViewSet):
    queryset = OfficeManager.objects.all()
    serializer_class = OfficeManagerSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']

    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return DoctorSerializer
        return DoctorListSerializer

    def destroy(self, request, *args, **kwargs):
        doctor = self.get_object()
        if doctor.patient.exists():
            raise ValidationError('У этого доктора еще есть пациенты!')
        else:
            doctor.is_active = False
            doctor.save()
        new_doctor = DoctorSerializer(doctor)
        return Response(new_doctor.data, status=status.HTTP_200_OK)


class ArchiveDoctorViewSet(DoctorViewSet):
    queryset = Doctor.objects.filter(is_active=False)

    def destroy(self, request, *args, **kwargs):
        doctor = self.get_object()
        doctor.is_active = True
        doctor.save()
        new_doctor = DoctorSerializer(doctor)
        return Response(new_doctor.data, status=status.HTTP_200_OK)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.filter(is_active=True)
    serializer_class = PatientSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']

    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'update']:
            return PatientSerializer
        return PatientListSerializer

    def destroy(self, request, *args, **kwargs):
        patient = self.get_object()
        patient.is_active = False
        patient.save()
        CheckList.objects.filter(patient=patient, is_archive=False).update(is_archive=True)
        MedCard.objects.filter(patient=patient, is_archive=False).update(is_archive=True)
        new_patient = PatientSerializer(patient)
        return Response(new_patient.data, status=status.HTTP_200_OK)


class ArchivePatientViewSet(PatientViewSet):
    queryset = Patient.objects.filter(is_active=False)

    def destroy(self, request, *args, **kwargs):
        patient = self.get_object()
        patient.is_active = True
        patient.save()
        template = CheckListTemplate.objects.latest('id')
        answer_data = CheckListTemplateListSerializer(template).data
        answers = []
        for i in answer_data['title']:
            for j in i['question']:
                answers.append(j['id'])
        for month in range(1, 10):
            a = CheckList.objects.create(month=month, doctor_id=patient.doctor_field.id, patient_id=patient.pk,
                                         template=template)
            for question_id in answers:
                Answer.objects.create(question_id=question_id, check_list=a)
        new_patient = PatientSerializer(patient)
        MedCard.objects.create(patient=patient)
        return Response(new_patient.data, status=status.HTTP_200_OK)


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=True)
    serializer_class = AdminSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Patient')  # this will make a sheet named Users Data
    ws1 = wb.add_sheet('Users Doctor')
    # Sheet header, first row
    row_num = 0
    row_num1 = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        'First name',
        'Last name',
        'Birth date',
        'Email address',
        'Phone',
        'Address',
        'Inn',
        'Date of pregnancy',

    ]
    columns1 = [
        'First name',
        'Last name',
        'Birth date',
        'Email address',
        'Phone',
        'Address',
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column
    for col_num in range(len(columns1)):
        ws1.write(row_num, col_num, columns1[col_num], font_style)  # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Patient.objects.all().values_list('first_name',
                                             'last_name',
                                             'birth_date',
                                             'email',
                                             'phone',
                                             'address',
                                             'inn',
                                             'date_of_pregnancy',
                                             )

    rows1 = Doctor.objects.all().values_list('first_name',
                                             'last_name',
                                             'birth_date',
                                             'email',
                                             'phone',
                                             'address',
                                             )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    for row in rows1:
        row_num1 += 1
        for col_num in range(len(row)):
            ws1.write(row_num1, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response
