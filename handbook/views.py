from django import views
from django.shortcuts import render
from rest_framework import viewsets

from handbook.serializers import *
from .models import *
# Create your views here.

class HandBookViewSet(viewsets.ModelViewSet):
    serializer_class=HandBookSerializer
    queryset=HandBook.objects.all()

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class=TodoSerializer
    queryset=Todo.objects.all()

class EssentialsViewSet(viewsets.ModelViewSet):
    serializer_class=EssentialsSerializer
    queryset=Essentials.objects.all()