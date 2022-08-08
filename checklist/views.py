from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Title,
    Question,
    MedCard,
    CheckList,
    Answer, CheckListTemplate
)
from .serializers import (
    TitleSerializer,
    MedCardSerializer,
    QuestionSerializer,
    CheckListSerializer,
    AnswerSerializer, TitleListSerializer, CheckListListSerializer, CheckListTemplateSerializer,
    CheckListTemplateListSerializer,
)


class TitleView(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleSerializer

class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()



class MedCardView(viewsets.ModelViewSet):
    serializer_class = MedCardSerializer
    queryset = MedCard.objects.all()


class CheckListView(viewsets.ModelViewSet):
    serializer_class = CheckListSerializer
    queryset = CheckList.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return CheckListListSerializer
        return CheckListSerializer


class CheckListTemplateView(viewsets.ModelViewSet):
    serializer_class = CheckListTemplateSerializer
    queryset = CheckListTemplate.objects.filter(id=1)
    # http_method_names = ['get', 'put']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return CheckListTemplateListSerializer
        return CheckListTemplateSerializer



class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()



