from django.db.models import Q
from rest_framework import serializers
from .models import (
    Schedule,
    Appointment,
    WorkDate,
)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            'id',
            'work_date',
            'doctor',
        ]


class WorkDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDate
        fields = [
            'id',
            'date',
            'start',
            'end',
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'disease',
            'content',
            'date',
            'start_time',
            'end_time',
            'doctor',
            'patient'
        ]

    def validate(self, data):
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if not WorkDate.objects.filter(date=date).filter(start__lte=start_time).filter(end__gte=end_time).exists():
            raise serializers.ValidationError('The doctor is not working at this time!')
        if Appointment.objects.filter(Q(start_time__range=[start_time, end_time]), date=date).exists():
            raise serializers.ValidationError('This time is already booked!')
        elif Appointment.objects.filter(Q(end_time__range=[start_time, end_time]), date=date).exists():
            raise serializers.ValidationError('This time is already booked!')

        return data