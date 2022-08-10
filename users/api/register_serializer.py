from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from users.models import OfficeManager, Patient, Doctor


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
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = OfficeManager(**data)
        # get the password from the data
        password = data.get('password')
        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterOfficeManagerSerializer, self).validate(data)

    def validate_email(self, value):
        if value is None:
            raise serializers.ValidationError('Это поле не может быть пустым.')
        return value

    def validate_phone(self, value):
        if not value[1:].isnumeric():
            raise serializers.ValidationError('Phone must be numeric symbols')
        if value[:4] != '+996':
            raise serializers.ValidationError('Phone number should start with +996 ')
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = OfficeManager(**validated_data)
        user.set_password(password)
        user.save()
        return user


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
        if not value[1:].isnumeric():
            raise serializers.ValidationError('Phone must be numeric symbols')
        if value[:4] != '+996':
            raise serializers.ValidationError('Phone number should start with +996 ')
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return value

    def validate_inn(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError('INN must be numeric symbols')
        return value

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
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        # print(data)
        user = Doctor(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterDoctorSerializer, self).validate(data)

    def validate_phone(self, value):
        if not value[1:].isnumeric():
            raise serializers.ValidationError('Phone must be numeric symbols')
        if value[:4] != '+996':
            raise serializers.ValidationError('Phone number should start with +996 ')
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return value

    def validate_email(self, value):
        if value is None:
            raise serializers.ValidationError('Это поле не может быть пустым.')
        return value

    def create(self, validated_data):
        print(validated_data)
        if validated_data['email'] is None:
            raise serializers.ValidationError('asdfsad')
        password = validated_data.pop('password')
        user = Doctor(**validated_data)
        user.set_password(password)
        user.save()
        return user
