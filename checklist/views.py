from requests import Response
from rest_framework import viewsets, status
from .models import (
    Title,
    Option,
    MedCard,
    CheckList,
    Pattern,
)
from .serializers import (
    TitleSerializer,
    OptionSerializer,
    MedCardSerializer,
    CheckListSerializer,
    # CheckListSerializerForList,
    # PatternSerializerForList,
    PatternSerializer,
)


class TitleView(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()


class OptionView(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()


class MedCardView(viewsets.ModelViewSet):
    serializer_class = MedCardSerializer
    queryset = MedCard.objects.all()


class CheckListView(viewsets.ModelViewSet):
    serializer_class = CheckListSerializer
    queryset = CheckList.objects.all()

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return CheckListSerializerForList
    #     # elif self.action == 'update':
    #     #     return CheckListSerializerForList
    #     if self.action == 'list':
    #         return CheckListSerializerForList
    #     return CheckListSerializer

class PatternView(viewsets.ModelViewSet):
    serializer_class = PatternSerializer
    queryset = Pattern.objects.all()

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return PatternSerializerForList
    #     # elif self.action == 'update':
    #     #     return CheckListSerializerForList
    #     if self.action == 'list':
    #         return PatternSerializerForList
    #     return PatternSerializer