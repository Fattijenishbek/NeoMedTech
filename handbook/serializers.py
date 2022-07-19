from rest_framework import serializers

from .models import Todo, Essentials, Article, Handbook


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class TodoListSerializer(TodoSerializer):
    patient = serializers.StringRelatedField()


class EssentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essentials
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class HandBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handbook
        fields = '__all__'
