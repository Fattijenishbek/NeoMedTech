from rest_framework import serializers
from users.models import (
    Doctor,
    Patient,
)


class PersonalLoginWebSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = Doctor
        fields = ["email", "password"]


class PatientLoginMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["phone"]
