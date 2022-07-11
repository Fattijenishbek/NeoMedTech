from django.db.models import Q
from rest_framework import serializers

from users.models import Patient, Doctor
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
            'record',
            'inn',
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
        doc = data.get('doctor')
        inn = data.get('inn')

        if not Patient.objects.get(inn=inn):
            raise serializers.ValidationError("The inn doesn't match!")
        
        if not Schedule.objects.filter(doctor_id=doc.id, work_date__date=date, work_date__start__lte=start_time,
                                       work_date__end__gte=end_time).exists():
            raise serializers.ValidationError('The doctor is not working at this time!')
        if Appointment.objects.filter(Q(start_time__range=[start_time, end_time]), date=date,
                                      doctor_id=doc.id).exists():
            raise serializers.ValidationError('This time is already booked!')
        elif Appointment.objects.filter(Q(end_time__range=[start_time, end_time]), date=date,
                                        doctor_id=doc.id).exists():
            raise serializers.ValidationError('This time is already booked!')
        return data