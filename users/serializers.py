from rest_framework import serializers
from .models import User, Doctor, Patient
from .services import ModelSerializerWithValidate


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


class PatientSerializer(serializers.ModelSerializer):
    week_of_pregnancy = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        exclude = ['user']

    def validate(self, data):
        inn = data.get('inn')
        if len(inn) != 14:
            raise serializers.ValidationError('Your length of inn should be 14 characters!!!')
        return data


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
            "phone": {"required": True},
            "image": {"required": False},
            'birth_date': {'required': True},
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
            'image',
            "birth_date",
            "date_joined",
            "email",
            "user_type",
        ]
        read_only_fields = ["date_joined"]


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['resign',
                  'education',
                  'professional_sphere',
                  'work_experience',
                  'achievements']


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
            'email',
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
