from rest_framework import serializers
from .models import MedCard, CheckList, Answer, Question, Title, CheckListTemplate


class MedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedCard
        fields = [
            'patient',
            'information',
        ]


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


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        fields = ['id',
                  'name',
                  'is_ok',
                  'question'
                  ]
        model = Answer


class CheckListSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = CheckList

    def create(self, validated_data):
        answers = validated_data.pop('answer')
        check_list = CheckList.objects.create(**validated_data)
        for answer in answers:
            Answer.objects.create(**answer, check_list=check_list)
        return check_list


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class TitleCheckListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    question = QuestionListSerializer(many=True)

    class Meta:
        model = Title
        fields = ['id',
                  'name',
                  'question']

    def create(self, validated_data):
        questions_data = validated_data.pop('question')
        title = Title.objects.create(**validated_data)
        questions = []
        print(questions_data)
        for question_data in questions_data:
            question_id = question_data.pop('id', None)
            question, _ = Question.objects.get_or_create(id=question_id, defaults=question_data)
            questions.append(question)
        title.question.add(*questions)
        return title

    def update(self, instance, validated_data):
        questions = validated_data.pop('question', [])
        instance = super().update(instance, validated_data)
        for question in questions:
            question = Question.objects.get(pk=question.get('id'))
            instance.questions.add(question)
        return instance


class CheckListTemplateListSerializer(serializers.ModelSerializer):
    title = TitleCheckListSerializer(many=True)

    class Meta:
        model = CheckListTemplate
        fields = ['id',
                  'title']

    def create(self, validated_data):
        titles_data = validated_data.pop('title')
        template = CheckListTemplate.objects.create(**validated_data)
        titles = []
        for i in titles_data:
            questions_data = i.pop('question')
            title = Title.objects.create(**i)
            titles.append(title)
            questions = []
            for question_data in questions_data:
                question_id = question_data.pop('id', None)
                question, _ = Question.objects.get_or_create(id=question_id, defaults=question_data)
                questions.append(question)
            title.question.add(*questions)
            template.title.add(title)
        return template


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


class AnswerInCheckListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Answer
        fields = ['id',
                  'name',
                  'is_ok']


class CheckListPutSerializer(serializers.ModelSerializer):
    answer = AnswerInCheckListSerializer(many=True)

    class Meta:
        model = CheckList
        fields = ['id',
                  'answer',
                  'recommendations']

    def update(self, instance, validated_data):
        answers = validated_data.pop('answer')
        instance.recommendations = validated_data.get('recommendations', instance.recommendations)
        instance.save()
        keep_answers = []
        for answer in answers:
            if "id" in answer.keys():
                if Answer.objects.filter(id=answer['id']).exists():
                    c = Answer.objects.get(id=answer['id'])
                    c.is_ok = answer.get('is_ok', c.is_ok)
                    c.name = answer.get('name', c.name)
                    c.save()
                    keep_answers.append(c.id)
                else:
                    continue
            else:
                c = Answer.objects.create(**answer)
                keep_answers.append(c.id)
        for answer in answers:
            if answer.get('id') not in keep_answers:
                Answer.objects.filter(id=answer.get('id')).delete()
        return instance
