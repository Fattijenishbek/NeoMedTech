from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from rest_framework import serializers
from django.utils.encoding import force_text
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .models import User, Doctor, Patient

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        if data['phone'][:4] != '+996':
            raise serializers.ValidationError('Value should be +996 ')

        return data


class RegisterPatientSerializer(serializers.ModelSerializer):
    user_type = serializers.HiddenField(default='patient')

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
        ]

        extra_kwargs = {
            "phone": {"required": True, "max_length": 13},
            "user_type": {"required": True},
            "image": {"required": False}
        }
        read_only_fields = ["is_active"]

    def validate(self, data):
        if data['phone'][:4] != '+996':
            raise serializers.ValidationError('Value should be +996 ')

        return data


class LoginWebSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class LoginMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone"]


class UserSerializer(serializers.ModelSerializer):
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


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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

    def custom_validation(self, attrs):
        pass

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
