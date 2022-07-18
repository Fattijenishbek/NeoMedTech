from datetime import date

from rest_framework import serializers


class ModelSerializerWithValidate(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def validate(self, data):
        if data['phone'][:4] != '+996':
            raise serializers.ValidationError('Phone number should start with +996 ')
        elif len(data['phone']) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return data

    def get_age(self, obj):
        today = date.today()
        return today.year - obj.birth_date.year - (
                (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
