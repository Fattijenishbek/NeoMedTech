import itertools
from datetime import datetime

from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Schedule,
    Appointment,
    TimeSlots, Holidays,
)
from .serializers import (
    ScheduleSerializer,
    ScheduleListSerializer,
    AppointmentSerializer,
    AppointmentListSerializer,
    TimeSlotsSerializer, AppointmentForBookingSerializer,
    AppointmentGetTimesSerializer,
    HolidaySerializer,
    ScheduleForBookingSerializer
)


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ScheduleListSerializer
        return ScheduleSerializer


class GetFreeTimeViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentForBookingSerializer
    queryset = Appointment.objects.all()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        appointment_serializer = AppointmentForBookingSerializer(data=request.data)
        if appointment_serializer.is_valid():
            doctor = request.data['doctor']
            date = request.data['date']
            if Holidays.objects.filter(doctor=doctor, day=date).exists():
                return Response({'Response': f'This doctor is resting on this day.'})
            query = Schedule.objects.filter(doctor=doctor)
            if not query.exists():
                return Response({'Response': f'This doctor does not working that day.'})
            week_day = f"{datetime.strptime(date, '%Y-%m-%d').strftime('%A').lower()}"

            serializer = ScheduleForBookingSerializer(query, many=True)

            query2 = Appointment.objects.filter(doctor=doctor, date=date)
            serializer2 = AppointmentGetTimesSerializer(query2, many=True)
            free_times = serializer.data[0][week_day]
            booked_times = [i['time_slots'] for i in serializer2.data]

            res = list(itertools.filterfalse(lambda i: i in booked_times, free_times)) \
                  + list(itertools.filterfalse(lambda j: j in free_times, booked_times))

            return Response({
                'doctor': doctor,
                'date': request.data['date'],
                'free times': res,
                'booked times': booked_times,
            })
        return Response(appointment_serializer.errors)


class TimeSlotsView(viewsets.ModelViewSet):
    serializer_class = TimeSlotsSerializer
    queryset = TimeSlots.objects.all()


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AppointmentListSerializer
        return AppointmentSerializer


class HolidayViewSet(viewsets.ModelViewSet):
    serializer_class = HolidaySerializer
    queryset = Holidays.objects.all()
