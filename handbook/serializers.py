from datetime import timedelta
import datetime

from rest_framework import serializers

from .models import Todo, Essentials, Article, Handbook, FAQ


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
    dates_of_advices = serializers.SerializerMethodField()

    class Meta:
        model = Handbook
        fields = '__all__'

    def get_dates_of_advices(self, obj):
        today = datetime.date.today()
        list_of_month = [
            'января',
            'февраля',
            'марта',
            'апреля',
            'мая',
            'июня',
            'июля',
            'августа',
            'сентября',
            'октября',
            'ноября',
            'декабря'
        ]
        weekday = today.weekday()
        six = timedelta(days=6)
        monday = today - datetime.timedelta(days=weekday % 7)
        sunday = today - datetime.timedelta(days=weekday % 7) + six
        return f"{monday.day}-{sunday.day} {list_of_month[today.month - 1]}"





class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
