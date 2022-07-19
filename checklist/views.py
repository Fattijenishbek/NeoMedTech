from rest_framework import viewsets
from rest_framework.response import Response

from .models import Question, Answer, MedCard, CheckList
from .serializers import QuestionSerializer, AnswerSerializer, AnswerListSerializer, MedCardSerializer, \
    MedCardListSerializer, CheckListSerializer


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = AnswerListSerializer(Answer.objects.all(), many=True)
        return Response(serializer.data)


class MedCardView(viewsets.ModelViewSet):
    serializer_class = MedCardSerializer
    queryset = MedCard.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = MedCardListSerializer(MedCard.objects.all(), many=True)
        return Response(serializer.data)


class CheckListView(viewsets.ModelViewSet):
    serializer_class = CheckListSerializer
    queryset = CheckList.objects.all()
