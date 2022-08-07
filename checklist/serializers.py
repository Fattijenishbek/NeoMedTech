from rest_framework import serializers

from .models import MedCard, CheckList, Answer, Question, Title


class MedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedCard
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


class TitleListSerializer(TitleSerializer):
    question = QuestionSerializer(many=True)


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CheckList


class AnswerSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
    class Meta:
        fields = '__all__'
        model = Answer


class QuestionListSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class TitleCheckListSerializer(TitleSerializer):
    question = QuestionListSerializer(many=True)


class CheckListListSerializer(CheckListSerializer):
    title = TitleCheckListSerializer(many=True)
    # answer = AnswerSerializer(many=True)




