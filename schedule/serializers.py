import datetime

from rest_framework import serializers

from users.models import Patient, Doctor
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


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ['id']


class ScheduleListSerializer(ScheduleSerializer):
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


class AppointmentCreateByPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ['doctor', 'patient']

    def create(self, validated_data):
        user = self.context['request'].user
        patient = Patient.objects.get(id=user.pk)
        doctor = patient.doctor_field
        validated_data['patient'] = patient
        validated_data['doctor'] = doctor
        return Appointment.objects.create(**validated_data)


class AppointmentCreateByDoctorSerializer(AppointmentSerializer):
    class Meta:
        model = Appointment
        exclude = ['doctor']

    def create(self, validated_data):
        doctor = self.context['request'].user.pk
        validated_data['doctor'] = Doctor.objects.get(id=doctor)
        return Appointment.objects.create(**validated_data)

    def validate_patient(self, patient):
        doctor = self.context['request'].user.pk
        if doctor == Patient.objects.get(id=patient.id).doctor_field.pk:
            return patient
        else:
            raise serializers.ValidationError("Это не ваш пациент")


class AppointmentForBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date']

    def validate_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError('This day is already in the past')
        return value


class AppointmentGetTimesSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotsSerializer()

    class Meta:
        model = Appointment
        fields = ['time_slots', 'patient']


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holidays
        fields = '__all__'


class AppointmentOfDoctorForWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date']
