from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "phone",
            "user_type",
            "password",
            "address",
            "is_active",
        )
        read_only_fields = ['is_active']
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone": {"required": True},
            "user_type": {"required": True},
            "password": {"write_only": True},
        }

        def create(self, validated_data):
            user = User.objects.create(
                phone=validated_data["phone"],
                username=validated_data["username"],
                user_type=validated_data["user_type"],
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                address=validated_data["address"],
            )
            user.set_password(validated_data["password"])
            user.save()

            return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "password", "username"]