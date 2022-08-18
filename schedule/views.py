import itertools
from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from users.models import Doctor
from .models import (
    Schedule,
    Appointment,
    TimeSlots, Holidays,
)
from .serializers import (
    ScheduleSerializer,
    ScheduleListSerializer,
    AppointmentCreateByPatientSerializer,
    TimeSlotsSerializer,
    AppointmentForBookingSerializer,
    AppointmentGetTimesSerializer,
    HolidaySerializer,
    ScheduleForBookingSerializer,
    AppointmentSerializer,
    AppointmentCreateByDoctorSerializer,
    AppointmentOfDoctorForWeekSerializer, GetDoctorScheduleForOneDaySerializer, DatePostSerializer,
)
from users.permissions import (
    IsSuperUserOrOfficeManager,
    IsPatientOrIsDoctor
)


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()
    lookup_field = 'doctor'

    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ScheduleListSerializer
        return ScheduleSerializer


class GetFreeTimeViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentForBookingSerializer
    queryset = Appointment.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        appointment_serializer = AppointmentForBookingSerializer(data=request.data)
        if appointment_serializer.is_valid():
            doctor = request.data['doctor']
            date = request.data['date']
            if datetime.today() > datetime.strptime(date, '%Y-%m-%d'):
                return Response({'Response': 'Этот день уже в прошлом'},
                                status=status.HTTP_400_BAD_REQUEST)
            if Holidays.objects.filter(doctor=doctor, day=date).exists():
                return Response({'Response': f'В этот день доктор не работает.'},
                                status=status.HTTP_400_BAD_REQUEST)
            query = Schedule.objects.filter(doctor=doctor)
            week_day = f"{datetime.strptime(date, '%Y-%m-%d').strftime('%A').lower()}"

            if not query.exists() or not getattr(query[0], f'{week_day}').exists():
                return Response({'Response': f'В этот день доктор не работает.'},
                                status=status.HTTP_400_BAD_REQUEST)

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
                'free_times': res,
                'booked_times': booked_times,
            })
        return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimeSlotsView(viewsets.ModelViewSet):
    serializer_class = TimeSlotsSerializer
    queryset = TimeSlots.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['date', ]

    # permission_classes = (IsAuthenticatedOrReadOnly, )
    #                       IsPatientOrIsDoctor,)

    def get_serializer_class(self):
        if self.action == 'create':
            if not self.request.user.is_anonymous:
                if self.request.user.user_type == 'doctor':
                    return AppointmentCreateByDoctorSerializer
                elif self.request.user.user_type == 'patient':
                    return AppointmentCreateByPatientSerializer
        return AppointmentSerializer




class HolidayViewSet(viewsets.ModelViewSet):
    serializer_class = HolidaySerializer
    queryset = Holidays.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)


class AppointmentOfDoctorForWeekViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentOfDoctorForWeekSerializer
    queryset = Appointment.objects.all()
    http_method_names = ['post']

    # permission_classes = (IsAuthenticatedOrReadOnly,
    #                       IsSuperUserOrOfficeManager,)

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
                    'free_times': res,
                    'booked_times': serializer2.data,
                })
                monday += timedelta(days=1)
            return Response(response, status=status.HTTP_200_OK)
        return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDoctorScheduleForOneDayViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = GetDoctorScheduleForOneDaySerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = GetDoctorScheduleForOneDaySerializer(data=request.data, instance=Doctor.objects.all(), many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
