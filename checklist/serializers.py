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


class QuestionAnswerSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()
    class Meta:
        model = models.Answer
        fields = ['answer', 'question']


class MedCardListSerializer(MedCardSerializer):
    answer = QuestionAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = models.MedCard
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheckList
        fields = '__all__'
