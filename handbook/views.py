from django import views
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from handbook.serializers import *
from .models import *


# Create your views here.

class HandBookViewSet(viewsets.ModelViewSet):
    serializer_class = HandBookSerializer
    queryset = Handbook.objects.all()


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = TodoListSerializer(Todo.objects.all(), many=True)
        return Response(serializer.data)

class EssentialsViewSet(viewsets.ModelViewSet):
    serializer_class = EssentialsSerializer
    queryset = Essentials.objects.all()


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()