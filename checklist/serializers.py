from rest_framework import serializers
from . import models


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'


class AnswerListSerializer(AnswerSerializer):
    patient = serializers.StringRelatedField()
    question = serializers.StringRelatedField()


class MedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedCard
        fields = '__all__'


class MedCardListSerializer(MedCardSerializer):
    question = serializers.StringRelatedField(many=True)


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheckList
        fields = '__all__'
