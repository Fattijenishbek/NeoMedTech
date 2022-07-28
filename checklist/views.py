from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Question,
    Option,
    MedCard,
    CheckList,
    Check,
)
from .serializers import (
    QuestionSerializer,
    OptionSerializer,
    CheckSerializer,
    MedCardSerializer,
    CheckListSerializer,
)


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class OptionView(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()


class MedCardView(viewsets.ModelViewSet):
    serializer_class = MedCardSerializer
    queryset = MedCard.objects.all()


class CheckListView(viewsets.ModelViewSet):
    serializer_class = CheckListSerializer
    queryset = CheckList.objects.all()


class CheckView(viewsets.ModelViewSet):
    serializer_class = CheckSerializer
    queryset = Check.objects.all()