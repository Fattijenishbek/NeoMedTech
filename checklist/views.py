from rest_framework import viewsets, generics
from rest_framework.response import Response

from .models import (
    Title,
    Question,
    MedCard,
    CheckList,
    Answer
)
from .serializers import (
    TitleSerializer,
    MedCardSerializer,
    QuestionSerializer,
    CheckListSerializer,
    AnswerSerializer, TitleListSerializer, CheckListListSerializer,
)
from users.permissions import (
    IsSuperUserOrOfficeManager,
    IsSuperUserOrOfficeManagerOrDoctor,
)


class TitleView(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    permission_classes = (IsSuperUserOrOfficeManager,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleSerializer


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsSuperUserOrOfficeManager,)


class MedCardView(viewsets.ModelViewSet):
    serializer_class = MedCardSerializer
    queryset = MedCard.objects.all()
    lookup_field = 'patient'


class CheckListView(viewsets.ModelViewSet):
    serializer_class = CheckListSerializer
    queryset = CheckList.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CheckListListSerializer
        return CheckListSerializer


class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
