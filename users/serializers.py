from datetime import date

from rest_framework import serializers

from .models import User


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
        read_only_fields = ['user_type', "is_active"]

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
    age = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "phone",
            "birth_date",
            "date_joined",
            "email",
            "user_type",
            "age",
        ]
        read_only_fields = ["date_joined"]

    @staticmethod
    def get_age(obj):
        today = date.today()
        return today.year - obj.birth_date.year - (
                    (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))


