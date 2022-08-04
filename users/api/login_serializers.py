from rest_framework import serializers
from users.models import Doctor, Patient, OfficeManager


class DoctorLoginWebSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["email", "password"]


class PatientLoginMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["phone"]


class OfficeManagerLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeManager
        fields = ['email', 'password']
