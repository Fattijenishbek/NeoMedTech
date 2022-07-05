from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from . import serializers as ser
from . import models


class QuestionView(viewsets.ModelViewSet):
    serializer_class = ser.QuestionSerializer
    queryset = models.Question.objects.all()


class AnswerView(viewsets.ModelViewSet):
    serializer_class = ser.AnswerSerializer
    queryset = models.Answer.objects.all()


    def list(self, request, *args, **kwargs):
        serializer = ser.AnswerListSerializer(models.Answer.objects.all(), many=True)
        return Response(serializer.data)


class MedCardView(viewsets.ModelViewSet):
    serializer_class = ser.MedCardSerializer
    queryset = models.MedCard.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = ser.MedCardListSerializer(models.MedCard.objects.all(), many=True)
        return Response(serializer.data)


class CheckListView(viewsets.ModelViewSet):
    serializer_class = ser.CheckListSerializer
    queryset = models.CheckList.objects.all()
