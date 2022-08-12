from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
    AnswerSerializer,
    TitleListSerializer,
    CheckListListSerializer,
    CheckListTemplateListSerializer,
    TitleCheckListSerializer,
    CheckListPutSerializer,
)
from users.permissions import (
    IsSuperUserOrOfficeManager,
    IsSuperUserOrOfficeManagerOrDoctor,
)


class TitleView(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManager,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleCheckListSerializer


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManager,)


class MedCardView(viewsets.ModelViewSet):
    serializer_class = MedCardSerializer
    queryset = MedCard.objects.all()
    lookup_field = 'patient'
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManagerOrDoctor,)


class CheckListView(viewsets.ModelViewSet):
    serializer_class = CheckListSerializer
    queryset = CheckList.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['patient', 'month']
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManagerOrDoctor,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return CheckListListSerializer
        elif self.action == 'update':
            return CheckListPutSerializer
        return CheckListSerializer


class CheckListTemplateView(viewsets.ModelViewSet):
    serializer_class = CheckListTemplateListSerializer
    queryset = CheckListTemplate.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManager,)


class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrOfficeManagerOrDoctor, )
