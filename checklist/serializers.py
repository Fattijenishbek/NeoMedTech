from rest_framework import serializers

from .models import (
    CheckList,
    MedCard,
    Option,
    Title,
    Pattern,
)


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = '__all__'


class TitleSerializerList(serializers.ListSerializer):

    def update(self, instance, validated_data):
        nested_serializer = self.fields['header']
        nested_instance = instance.header
        nested_data = validated_data.pop('header')
        nested_serializer.update(nested_instance, nested_data)
        return super(TitleSerializerList, self).update(instance, validated_data)


class TitleSerializer(serializers.ModelSerializer):
    header = OptionSerializer(many=True)

    class Meta:
        model = Title
        list_serializer_class = TitleSerializerList
        fields = [
            'id',
            'title',
            'header',
        ]
    # def create(self, validated_data):
    #     titles = validated_data.pop('titles_set')
    #     title = Title.objects.create(**validated_data)
    #     for title in titles:
    #         Option.objects.create(title=title, **title)

        # for branch in branches:
        #     Branch.objects.create(course=course, **branch)

        # return title


class PatternSerializer(serializers.ModelSerializer):
    titles = TitleSerializer(many=True)

    class Meta:
        model = Pattern
        fields = [
            "id",
            'titles',
            'recommendation',
        ]
    #
    # def update(self, instance, validated_data):
    #     nested_serializer = self.fields['titles']
    #     nested_instance = instance.titles
    #     nested_data = validated_data.pop('titles')
    #     nested_serializer.update(nested_instance, nested_data)
    #     return super(PatternSerializer, self).update(instance, validated_data)
    #

# class PatternSerializerForList(PatternSerializer):


class MedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedCard
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    pattern = PatternSerializer()

    class Meta:
        model = CheckList
        fields = [
            'id',
            'doctor',
            'patient',
            'pattern',
        ]

    def create(self, validated_data):
        instance = CheckList.objects.create(**validated_data)

        for i in range(1, 9):
            CheckList.objects.create(**validated_data)
        return instance


# class CheckListSerializerForList(CheckListSerializer):
#
#     pattern = PatternSerializerForList()

    # def create(self, validated_data):
    #     pat = validated_data.pop('pattern')
    #     check_list = CheckList.objects.create(**validated_data)
    #     for i in range(0, 10):
    #         CheckList.objects.create(**validated_data)
    #         for i in pat:
    #             Pattern.objects.create(pattern=self.pk, **i)
    #
    #     return check_list

#
#     # def create(self, validated_data):
#     #     titles_data = validated_data.pop('titles')
#     #     check_list = CheckList.objects.create(**validated_data)
#     #     Title.objects.create(title=check_list, **titles_data)
#     #     return check_list

