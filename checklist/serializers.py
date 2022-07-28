from rest_framework import serializers

from .models import (
    CheckList,
    MedCard,
    Option,
    Title,
)


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    answers = OptionSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = [
            'id',
            'title',
            'check_list',
            'answers',
        ]


class MedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedCard
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    titles = TitleSerializer(read_only=True, many=True)

    class Meta:
        model = CheckList
        fields = [
            'doctor',
            'patient',
            'titles',
        ]
