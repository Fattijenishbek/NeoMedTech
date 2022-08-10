from rest_framework import viewsets

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
    AnswerSerializer, TitleListSerializer, CheckListListSerializer,
    CheckListTemplateListSerializer, TitleCheckListSerializer, CheckListPutSerializer,
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
        return TitleCheckListSerializer




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

    def get_queryset(self):
        queryset = CheckList.objects.all()
        patient = self.request.query_params.get('patient', None)
        if patient:
            queryset = queryset.filter(patient_id=int(patient))
        return queryset

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


class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
