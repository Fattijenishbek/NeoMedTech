from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Handbook, Todo, Essentials, Article, FAQ
from .serializers import (
    HandBookSerializer,
    TodoSerializer,
    TodoListSerializer,
    EssentialsSerializer,
    ArticleSerializer,
    FAQSerializer,
)
from users.permissions import (
    IsSuperUserOrOfficeManager,
)


class HandBookViewSet(viewsets.ModelViewSet):
    serializer_class = HandBookSerializer
    queryset = Handbook.objects.all()
    permission_classes = (IsSuperUserOrOfficeManager,)
    lookup_field = 'week'


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
    permission_classes = (IsSuperUserOrOfficeManager,)
    queryset = Article.objects.all()


class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()
    permission_classes = (IsSuperUserOrOfficeManager,)
