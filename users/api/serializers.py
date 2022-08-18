from datetime import date, timedelta
from dateutil import relativedelta
from rest_framework import serializers

from schedule.serializers import AppointmentForVisitHistorySerializer
from users.models import User, Doctor, Patient, OfficeManager
from .custom_funcs import get_age, validate_inn


class PatientListSerializer(serializers.ModelSerializer):
    week_of_pregnancy = serializers.SerializerMethodField()
    month_of_pregnancy = serializers.SerializerMethodField()
    approximate_date_of_pregnancy = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    appointment = AppointmentForVisitHistorySerializer(many=True, read_only=True)
    class Meta:
        model = Patient
        fields = ['id',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'age',
                  'is_active',
                  'image',
                  'address',
                  'phone',
                  'date_of_pregnancy',
                  'inn',
                  'appointment',
                  'week_of_pregnancy',
                  'month_of_pregnancy',
                  'approximate_date_of_pregnancy',
                  'user_type',
                  'doctor_field'
                  ]
        read_only_fields = ['user_type', 'doctor_field', 'is_active']

    def get_age(self, obj):
        return get_age(obj)

    def validate_inn(self, value):
        return validate_inn(value)

    def get_week_of_pregnancy(self, obj):
        days = abs(obj.date_of_pregnancy - date.today()).days
        return days // 7 + 1

    def get_month_of_pregnancy(self, obj):
        pregnancy_date = obj.date_of_pregnancy
        today = date.today()
        delta = relativedelta.relativedelta(today, pregnancy_date)
        return (delta.months + delta.years * 12) + 1

    def get_approximate_date_of_pregnancy(self, obj):
        res = obj.date_of_pregnancy + timedelta(days=270)
        return res.strftime('%d.%m.%Y')


class DoctorListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'age',
                  'image',
                  'address',
                  'phone',
                  'email',
                  'is_active',
                  'user_type',
                  'resign',
                  'education',
                  'professional_sphere',
                  'work_experience',
                  'achievements',
                  'patient',
                  ]
        read_only_fields = ['user_type', 'is_active']

    def get_age(self, obj):
        return get_age(obj)


class PatientSerializer(PatientListSerializer):
    doctor_field = DoctorListSerializer(read_only=True)


class DoctorSerializer(DoctorListSerializer):
    patient = serializers.SerializerMethodField()

    def get_patient(self, obj):
        patient = Patient.objects.filter(is_active=True, doctor_field=obj)
        serializer = PatientListSerializer(instance=patient, many=True)
        return serializer.data


class OfficeManagerSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = OfficeManager
        fields = ['id',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'age',
                  'email',
                  'image',
                  'address',
                  'phone',
                  'user_type',
                  ]

    def get_age(self, obj):
        return get_age(obj)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'user_type',
                  'email',
                  ]
    read_only_fields = ['user_type']