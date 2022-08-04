from datetime import date, timedelta
from dateutil import relativedelta
from rest_framework import serializers
from users.models import User, Doctor, Patient, OfficeManager


class PatientListSerializer(serializers.ModelSerializer):
    week_of_pregnancy = serializers.SerializerMethodField()
    month_of_pregnancy = serializers.SerializerMethodField()
    approximate_date_of_pregnancy = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'image',
                  'address',
                  'phone',
                  'date_of_pregnancy',
                  'inn',
                  'week_of_pregnancy',
                  'month_of_pregnancy',
                  'approximate_date_of_pregnancy',
                  'doctor_field'
                  ]

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
            res = obj.date_of_pregnancy + timedelta(days=270)
            return res.strftime('%d.%m.%Y')
        return None


class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'image',
                  'address',
                  'phone',
                  'email',
                  'resign',
                  'education',
                  'professional_sphere',
                  'work_experience',
                  'achievements',
                  'patient'
                  ]


class PatientSerializer(PatientListSerializer):
    doctor_field = DoctorListSerializer()


class DoctorSerializer(DoctorListSerializer):
    patient = PatientListSerializer(many=True, read_only=True)


class OfficeManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeManager
        fields = ['id',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'email',
                  'image',
                  'address',
                  'phone',
                  ]


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  ]
