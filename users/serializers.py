from datetime import date
from dateutil import relativedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from checklist.models import CheckList
from .models import User, Doctor, Patient
from .services import ModelSerializerWithValidate

UserModel = get_user_model()


class RegisterSerializer(ModelSerializerWithValidate):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "phone",
            "image",
            'password',
            "user_type",
            "address",
            "is_active",
        ]
        read_only_fields = ['is_active']
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
            "phone": {"required": True, "max_length": 13},
            "user_type": {"required": True},
            "image": {"required": False}
        }

    def create(self, validated_data):
        user = User.objects.create(
            user_type=validated_data["user_type"],
            email=validated_data["email"],
            birth_date=validated_data['birth_date'],
            phone=validated_data['phone'],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            address=validated_data["address"],
            image=validated_data["image"]
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class PatientSerializer(serializers.ModelSerializer):
    week_of_pregnancy = serializers.SerializerMethodField()
    month_of_pregnancy = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "id",
            "date_of_pregnancy",
            'inn',
            'approximate_date_of_birth',
            "week_of_pregnancy",
            "month_of_pregnancy",
            'doctor',
        ]
        extra_kwargs = {
            "date_of_pregnancy": {"required": True},
        }
        read_only_fields = ["approximate_date_of_birth"]


    def validate(self, data):
        inn = data.get('inn')
        if len(inn) != 14:
            raise serializers.ValidationError('Your length of inn should be 14 characters!!!')
        return data

    def get_week_of_pregnancy(self, obj):
        days = abs(obj.date_of_pregnancy - date.today()).days
        return days // 7

    def get_month_of_pregnancy(self, obj):
        pregnancy_date = obj.date_of_pregnancy
        today = date.today()
        delta = relativedelta.relativedelta(today, pregnancy_date)
        return delta.months + delta.years * 12

    def get_doctor(self, obj):

        patient_id = obj.id
        checklist = CheckList.objects.filter(patient__id=patient_id).last()

        return DoctorSimpleSerializer(checklist.doctor, many=False).data if checklist else None


class RegisterPatientSerializer(ModelSerializerWithValidate):
    user_type = serializers.HiddenField(default='patient')
    patient = PatientSerializer()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "image",
            "phone",
            "user_type",
            "address",
            "is_active",
            'patient',
        ]

        extra_kwargs = {
            "phone": {"required": True},
            "image": {"required": False},
            'birth_date': {'required': True},
        }
        read_only_fields = ["is_active"]

    def create(self, validated_data):
        patient_data = validated_data.pop('patient')
        user = User.objects.create(**validated_data)
        Patient.objects.create(user=user, **patient_data)
        return user


class LoginWebSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class LoginMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone"]


class UserSerializer(ModelSerializerWithValidate):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "phone",
            "image",
            "birth_date",
            "date_joined",
            "email",
            "user_type",
        ]
        read_only_fields = ["date_joined"]


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = [
            'id',
            'education',
            'professional_sphere',
            'work_experience',
            'achievements',
            # 'patients'
        ]


class DoctorSimpleProfileSerializer(ModelSerializerWithValidate):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "phone",
            'image',
            'age',
            "birth_date",
            "date_joined",
            "email",
            "user_type",
        ]
        read_only_fields = ["date_joined"]


class DoctorProfileSerializer(ModelSerializerWithValidate):
    doctor = DoctorSerializer()
    patients = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "phone",
            'image',
            'age',
            "birth_date",
            "date_joined",
            "email",
            "user_type",
            'doctor',
            'patients',
        ]
        read_only_fields = ["date_joined"]

    def update(self, instance, validated_data):
        nested_serializer = self.fields['doctor']
        nested_instance = instance.doctor
        nested_data = validated_data.pop('doctor')
        nested_serializer.update(nested_instance, nested_data)
        return super(DoctorProfileSerializer, self).update(instance, validated_data)

    def get_patients(self, obj):
        doctor_id = Doctor.objects.get(user__id=obj.id).id
        patient_ids = CheckList.objects.filter(doctor__id=doctor_id).values_list('patient_id', flat=True)
        patients = Patient.objects.filter(id__in=patient_ids)
        return PatientSimpleSerializer(patients, many=True).data


class DoctorSimpleSerializer(serializers.ModelSerializer):
    user = DoctorSimpleProfileSerializer()

    class Meta:
        model = Doctor
        fields = [
            'id',
            'education',
            'professional_sphere',
            'work_experience',
            'achievements',
            'user',
        ]


class PatientSimpleProfileSerializer(ModelSerializerWithValidate):
    user_type = serializers.HiddenField(default='patient')

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "phone",
            'image',
            'email',
            "birth_date",
            "date_joined",
            "user_type",
            "patient",
            'age',
        ]
        read_only_fields = ["date_joined"]


class PatientProfileSerializer(ModelSerializerWithValidate):
    patient = PatientSerializer()
    user_type = serializers.HiddenField(default='patient')

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "phone",
            'image',
            'email',
            "birth_date",
            "date_joined",
            "user_type",
            "patient",
            'age',
        ]
        read_only_fields = ["date_joined"]

    def update(self, instance, validated_data):
        nested_serializer = self.fields['patient']
        nested_instance = instance.patient
        nested_data = validated_data.pop('patient')
        nested_serializer.update(nested_instance, nested_data)
        return super(PatientProfileSerializer, self).update(instance, validated_data)


class PatientSimpleSerializer(serializers.ModelSerializer):
    user = PatientSimpleProfileSerializer()

    class Meta:
        model = Patient
        fields = '__all__'


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError('Error')

        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError('Invalid e-mail address')

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    uid = serializers.CharField(required=False)
    token = serializers.CharField(required=False)

    set_password_form_class = SetPasswordForm


    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        self.set_password_form.save()
