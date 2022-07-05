from rest_framework import serializers
from .models import *

class HandBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandBook
        fields = '__all__'

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class EssentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essentials
        fields = '__all__'