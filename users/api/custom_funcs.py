from datetime import date, timedelta
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from rest_framework.response import Response

from schedule.models import Schedule, Appointment, Holidays


def get_age(obj):
    today = date.today()
    return today.year - obj.birth_date.year - (
            (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))


def validate_phone(value):
    if not value[1:].isnumeric():
        raise serializers.ValidationError('Phone must be numeric symbols')
    if value[:4] != '+996':
        raise serializers.ValidationError('Phone number should start with +996 ')
    elif len(value) != 13:
        raise serializers.ValidationError("Phone number must be 13 characters long")
    return value


def validate_email(value):
    if value is None:
        raise serializers.ValidationError('Это поле не может быть пустым.')
    return value


def create(validated_data, model):
    password = validated_data.pop('password')
    user = model(**validated_data)
    user.set_password(password)
    user.save()
    return user


def validate(self, data, model, serializer):
    user = model(**data)
    password = data.get('password')
    errors = dict()
    try:
        validators.validate_password(password=password, user=user)
    except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)
    if errors:
        raise serializers.ValidationError(errors)
    return super(serializer, self).validate(data)


def validate_inn(value):
    if not value.isnumeric():
        raise serializers.ValidationError('INN must be numeric symbols')
    if len(value) != 14:
        raise serializers.ValidationError('Your length of inn should be 14 characters!!!')
    return value


def get_token(user):
    refresh = RefreshToken.for_user(user)
    expires_in = refresh.access_token.lifetime.total_seconds()
    expires_day = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
    return Response(
        {
            'user_id': user.id,
            "status": "You successfully logged in",
            "expires_day": expires_day,
            "is_superuser": user.is_superuser,
            "user_type": user.user_type,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    )


def validate_for_appointment(data, doctor):
    date = data['date']
    time_slots = data['time_slots']
    week_day = date.strftime('%A').lower()
    if datetime.date.today() > date:
        raise serializers.ValidationError('Этот день прошёл.')
    elif Holidays.objects.filter(doctor=doctor, day=date).exists():
        raise serializers.ValidationError('У доктора в этот день выходной.')
    elif datetime.date.today() == date:
        raise serializers.ValidationError('Бронирование на сегодняшний день недоступно.')
    if not Schedule.objects.filter(doctor=doctor).exists():
        raise serializers.ValidationError('Доктор без расписания')
    if time_slots not in getattr(Schedule.objects.get(doctor=doctor), week_day).all():
        raise serializers.ValidationError('Доктор в это время не работает.')
    if Appointment.objects.filter(doctor=doctor, date=date, time_slots=time_slots).exists():
        raise serializers.ValidationError('Это время уже забронировано.')
    return data
