import datetime

from rest_framework import serializers

from .models import (
    Schedule,
    Appointment,
    TimeSlots,
    Holidays
)


class TimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = '__all__'


class TimeSlotsListSerializer(serializers.ModelSerializer):
    times = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlots
        fields = ['id', 'times']

    def get_times(self, obj):
        return f'{obj.start} - {obj.end}'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleListSerializer(ScheduleSerializer):
    doctor = serializers.StringRelatedField()
    monday = serializers.StringRelatedField(many=True)
    tuesday = serializers.StringRelatedField(many=True)
    wednesday = serializers.StringRelatedField(many=True)
    thursday = serializers.StringRelatedField(many=True)
    friday = serializers.StringRelatedField(many=True)
    saturday = serializers.StringRelatedField(many=True)
    sunday = serializers.StringRelatedField(many=True)


class ScheduleForBookingSerializer(ScheduleSerializer):
    doctor = serializers.StringRelatedField()
    monday = TimeSlotsSerializer(many=True)
    tuesday = TimeSlotsSerializer(many=True)
    wednesday = TimeSlotsSerializer(many=True)
    thursday = TimeSlotsSerializer(many=True)
    friday = TimeSlotsSerializer(many=True)
    saturday = TimeSlotsSerializer(many=True)
    sunday = TimeSlotsSerializer(many=True)


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentForBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'date']

    def validate_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError('This day is already in the past')
        return value


class AppointmentListSerializer(AppointmentSerializer):
    doctor = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()
    time_slots = serializers.StringRelatedField()


class AppointmentGetTimesSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotsListSerializer()

    class Meta:
        model = Appointment
        fields = ['time_slots']


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holidays
        fields = '__all__'
