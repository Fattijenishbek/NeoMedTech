from rest_framework import serializers

from .models import (
    CheckList,
    Check,
    MedCard,
    Option,
    Question,
)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class CheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Check
        fields = '__all__'


# class ListCheckSerializer(CheckSerializer):
#     # a = QuestionSerializer(read_only=True, many=True)
#     # b = OptionSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = Check
#         fields = '__all__'


class MedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedCard
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    # check = CheckSerializer(read_only=True, many=True)

    class Meta:
        model = CheckList
        fields = '__all__'
