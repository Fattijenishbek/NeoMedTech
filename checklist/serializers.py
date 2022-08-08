from rest_framework import serializers

from .models import MedCard, CheckList, Answer, Question, Title, CheckListTemplate


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
    class Meta:
        fields = '__all__'
        model = Answer


class QuestionListSerializer(serializers.ModelSerializer):
    # answer = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class TitleCheckListSerializer(serializers.ModelSerializer):
    question = QuestionListSerializer(many=True)

    class Meta:
        model = Title
        fields = ['id',
                  'name',
                  'question']


class CheckListTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckListTemplate
        fields = ['title']


class CheckListTemplateListSerializer(CheckListTemplateSerializer):
    title = TitleCheckListSerializer(many=True)


class CheckListListSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True)
    template = CheckListTemplateListSerializer()

    class Meta:
        model = CheckList
        fields = ['id',
                  'month',
                  'doctor',
                  'patient',
                  'recommendations',
                  'answer',
                  'template',
                  ]
