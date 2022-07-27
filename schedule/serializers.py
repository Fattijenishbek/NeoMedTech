from rest_framework import serializers

from .models import (
    Schedule,
    Appointment,
    TimeSlots,
    WorkDays,
)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleListSerializer(ScheduleSerializer):
    work_days = serializers.StringRelatedField(many=True)
    doctor = serializers.StringRelatedField()


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentListSerializer(AppointmentSerializer):
    doctor = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()
    time_slots = serializers.StringRelatedField()


class TimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = '__all__'


class WorkDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDays
        fields = '__all__'


class WorkDaysListSerializer(WorkDaysSerializer):
    time_slots = TimeSlotsSerializer()
