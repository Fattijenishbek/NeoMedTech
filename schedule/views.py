import itertools
from datetime import datetime, timedelta

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (
    Schedule,
    Appointment,
    TimeSlots, Holidays,
)
from .serializers import (
    ScheduleSerializer,
    ScheduleListSerializer,
    AppointmentCreateByPatientSerializer,
    TimeSlotsSerializer, AppointmentForBookingSerializer,
    AppointmentGetTimesSerializer,
    HolidaySerializer,
    ScheduleForBookingSerializer, AppointmentSerializer, AppointmentCreateByDoctorSerializer,
    AppointmentOfDoctorForWeekSerializer,
)
from users.permissions import (
    IsSuperUserOrOfficeManager,
    IsPatientOrIsDoctor
)


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()
    lookup_field = 'doctor'
    permission_classes = (IsSuperUserOrOfficeManager,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ScheduleListSerializer
        return ScheduleSerializer


class GetFreeTimeViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentForBookingSerializer
    queryset = Appointment.objects.all()
    permission_classes = (AllowAny,)
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
    permission_classes = (IsSuperUserOrOfficeManager,)


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = (IsAuthenticated, IsPatientOrIsDoctor,)

    def get_serializer_class(self):
        if self.action == 'create':
            if self.request.user.user_type == 'doctor':
                return AppointmentCreateByDoctorSerializer
            elif self.request.user.user_type == 'patient':
                return AppointmentCreateByPatientSerializer
        return AppointmentSerializer


class HolidayViewSet(viewsets.ModelViewSet):
    serializer_class = HolidaySerializer
    queryset = Holidays.objects.all()
    permission_classes = (IsAuthenticated, IsSuperUserOrOfficeManager,)


class AppointmentOfDoctorForWeekViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentOfDoctorForWeekSerializer
    queryset = Appointment.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        appointment_serializer = AppointmentOfDoctorForWeekSerializer(data=request.data)
        if appointment_serializer.is_valid():
            doctor = request.data['doctor']
            date = request.data['date']
            weekday = datetime.strptime(date, '%Y-%m-%d').weekday()
            six = timedelta(days=6)
            monday = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=weekday % 7)
            sunday = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=weekday % 7) + six
            response = []
            query = Schedule.objects.filter(doctor=doctor)
            serializer = ScheduleForBookingSerializer(query, many=True)
            while monday <= sunday:
                if Holidays.objects.filter(doctor=doctor, day=monday).exists():
                    response.append({'Response': f'This doctor is resting on this day.'})
                    monday += timedelta(days=1)
                    continue

                if not query.exists():
                    response.append({'Response': f'This doctor does not working that day.'})
                    monday += timedelta(days=1)
                    continue
                week_day = f"{monday.strftime('%A').lower()}"
                query2 = Appointment.objects.filter(doctor=doctor, date=monday)
                serializer2 = AppointmentGetTimesSerializer(query2, many=True)
                free_times = serializer.data[0][week_day]
                booked_times = [i['time_slots'] for i in serializer2.data]
                res = list(itertools.filterfalse(lambda i: i in booked_times, free_times)) \
                      + list(itertools.filterfalse(lambda j: j in free_times, booked_times))
                response.append({
                    'doctor': int(doctor),
                    'date': monday.strftime('%d-%m-%Y'),
                    'free times': res,
                    'booked times': serializer2.data,
                })
                monday += timedelta(days=1)
            return Response(response, status=status.HTTP_200_OK)
        return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


