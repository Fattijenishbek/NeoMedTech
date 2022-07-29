from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Title,
    Option,
    MedCard,
    CheckList,
)
from .serializers import (
    TitleSerializer,
    OptionSerializer,
    MedCardSerializer,
    CheckListSerializer,
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
