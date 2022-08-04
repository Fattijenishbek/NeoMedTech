from datetime import date, timedelta
from dateutil import relativedelta
from django.conf import settings
from rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_text
# from django.utils.http import urlsafe_base64_decode as uid_decoder
from rest_framework import serializers
# from rest_framework.exceptions import ValidationError

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
            "phone": {"max_length": 13, 'min_length': 13},
        }

    def validate_email(self, value):
        if value is None:
            raise serializers.ValidationError('This field may not be blank.')
        return value

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
    approximate_date_of_pregnancy = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        exclude = ['user']

    def validate(self, data):
        inn = data.get('inn')
        if len(inn) != 14:
            raise serializers.ValidationError('Your length of inn should be 14 characters!!!')
        return data

    def get_week_of_pregnancy(self, obj):
        if obj.date_of_pregnancy:
            days = abs(obj.date_of_pregnancy - date.today()).days
            return days // 7 + 1
        return None

    def get_month_of_pregnancy(self, obj):
        if obj.date_of_pregnancy:
            pregnancy_date = obj.date_of_pregnancy
            today = date.today()
            delta = relativedelta.relativedelta(today, pregnancy_date)
            return delta.months + delta.years * 12
        return None

    def get_approximate_date_of_pregnancy(self, obj):
        if obj.date_of_pregnancy:
            return obj.date_of_pregnancy + timedelta(days=270)
        return None


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
            "image": {"required": False},
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
        read_only_fields = ["date_joined", 'user_type']

    def validate_email(self, value):
        if value is None:
            raise serializers.ValidationError('This field may not be blank.')
        return value


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
            "birth_date",
            "date_joined",
            "user_type",
            'patient',
            'age'
        ]
        read_only_fields = ["date_joined"]

    def update(self, instance, validated_data):
        nested_serializer = self.fields['patient']
        nested_instance = instance.patient
        nested_data = validated_data.pop('patient')
        nested_serializer.update(nested_instance, nested_data)
        return super(PatientProfileSerializer, self).update(instance, validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = ['education',
                  'professional_sphere',
                  'work_experience',
                  'achievements',
                  'patient']


class DoctorProfileSerializer(ModelSerializerWithValidate):
    doctor = DoctorSerializer()

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
            'doctor'
        ]
        read_only_fields = ["date_joined"]

    def update(self, instance, validated_data):
        nested_serializer = self.fields['doctor']
        nested_instance = instance.doctor
        nested_data = validated_data.pop('doctor')
        nested_serializer.update(nested_instance, nested_data)
        return super(DoctorProfileSerializer, self).update(instance, validated_data)


class PasswordResetSerializer(_PasswordResetSerializer):
    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),

            'email_template_name': 'reset_password.html',

            'request': request
        }
        self.reset_form.save(**opts)

