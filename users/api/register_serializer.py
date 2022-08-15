from rest_framework import serializers
from users.models import OfficeManager, Patient, Doctor
from .custom_funcs import validate_phone, validate_email, create, validate, validate_inn


class RegisterOfficeManagerSerializer(serializers.ModelSerializer):
    user_type = serializers.HiddenField(default='office_manager')
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = OfficeManager
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'password',
            'email',
            'image',
            'address',
            'phone',
            'user_type',
        ]

    def validate(self, data):
        return validate(self, data, OfficeManager, RegisterOfficeManagerSerializer)

    def validate_email(self, value):
        return validate_email(value)

    def validate_phone(self, value):
        return validate_phone(value)

    def create(self, validated_data):
        return create(validated_data, OfficeManager)


class RegisterPatientSerializer(serializers.ModelSerializer):
    user_type = serializers.HiddenField(default='patient')

    class Meta:
        model = Patient
        fields = ['first_name',
                  'last_name',
                  'birth_date',
                  'image',
                  'address',
                  'phone',
                  'date_of_pregnancy',
                  'inn',
                  'user_type',
                  'doctor_field'

                  ]
        extra_kwargs = {
            'inn': {'min_length': 14}
        }
        read_only_fields = ['is_active']

    def validate_phone(self, value):
        return validate_phone(value)

    def validate_inn(self, value):
        return validate_inn(value)

    def create(self, validated_data):
        user = Patient(**validated_data)
        user.save()
        return user


class RegisterDoctorSerializer(serializers.ModelSerializer):
    user_type = serializers.HiddenField(default='doctor')
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = Doctor
        fields = ['id',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'password',
                  'image',
                  'address',
                  'phone',
                  'email',
                  'user_type',
                  'resign',
                  'education',
                  'professional_sphere',
                  'work_experience',
                  'achievements',
                  ]

    def validate(self, data):
        return validate(self, data, Doctor, RegisterDoctorSerializer)

    def validate_phone(self, value):
        return validate_phone(value)

    def validate_email(self, value):
        return validate_email(value)

    def create(self, validated_data):
        return create(validated_data, Doctor)
