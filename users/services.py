from datetime import date

from rest_framework import serializers


class ModelSerializerWithValidate(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        today = date.today()
        return today.year - obj.birth_date.year - (
                (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))

    def validate_phone(self, value):
        if not value[1:].isnumeric():
            raise serializers.ValidationError('Phone must be numeric symbols')
        if value[:4] != '+996':
            raise serializers.ValidationError('Phone number should start with +996 ')
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return value