from django.db.models import DateTimeField
from django.db.models.functions import Trunc
from rest_framework import serializers
from users.api.custom_funcs import validate_for_appointment
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

    def validate(self, data):
        doctor = data['doctor']
        return validate_for_appointment(data=data, doctor=doctor)

    def validate_patient(self, patient):
        doctor = self.context['request'].data['doctor']
        if int(doctor) == patient.doctor_field.pk:
            return patient
        else:
            raise serializers.ValidationError("Это не ваш пациент")


class AppointmentCreateByPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ['doctor', 'patient']

    def create(self, validated_data):
        validated_data['patient'] = self.patient
        validated_data['doctor'] = self.doctor
        return Appointment.objects.create(**validated_data)

    def validate(self, attrs):
        user = self.context['request'].user
        self.patient = Patient.objects.get(id=user.pk)
        self.doctor = self.patient.doctor_field
        return validate_for_appointment(attrs, self.doctor)


class AppointmentCreateByDoctorSerializer(AppointmentSerializer):
    class Meta:
        model = Appointment
        exclude = ['doctor']

    def create(self, validated_data):
        validated_data['doctor'] = Doctor.objects.get(id=self.doctor)
        return Appointment.objects.create(**validated_data)

    def validate_patient(self, patient):
        self.doctor = self.context['request'].user.pk
        if self.doctor == patient.doctor_field.pk:
            return patient
        else:
            raise serializers.ValidationError("Это не ваш пациент")

    def validate(self, attrs):
        return validate_for_appointment(attrs, self.doctor)


class AppointmentForBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date']


class PatientAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id',
                  'first_name',
                  'last_name']


class AppointmentGetTimesSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotsSerializer()
    patient = PatientAppointmentSerializer()

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


class PatientForOneDayScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id',
                  'first_name',
                  'last_name',
                  'phone']


class AppointmentForOneDayScheduleSerializer(serializers.ModelSerializer):
    patient = PatientForOneDayScheduleSerializer()
    time_slots = TimeSlotsSerializer()

    class Meta:
        model = Appointment
        fields = ['id',
                  'date',
                  'patient',
                  'time_slots']


class GetDoctorScheduleForOneDaySerializer(serializers.ModelSerializer):
    appointment = serializers.SerializerMethodField()
    date = serializers.DateField(write_only=True)

    class Meta:
        model = Doctor
        fields = ['id',
                  'first_name',
                  'last_name',
                  'appointment',
                  'date']
        read_only_fields = ['id',
                            'first_name',
                            'last_name',
                            'appointment']

    def get_appointment(self, obj):
        date = self.initial_data['date']
        appointment = Appointment.objects.filter(date=date).order_by('time_slots_id')
        serializer = AppointmentForOneDayScheduleSerializer(instance=appointment, many=True)
        return serializer.data


class DatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id',
                  'first_name',
                  'last_name',
                  'appointment',
                  'date']
        read_only_fields = ['id',
                            'first_name',
                            'last_name',
                            'appointment']


class DoctorForVisitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id',
                  'first_name',
                  'last_name']


class AppointmentForVisitHistorySerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
    time_slots = TimeSlotsSerializer()

    class Meta:
        model = Appointment
        fields = ['id',
                  'date',
                  'doctor',
                  'time_slots']
