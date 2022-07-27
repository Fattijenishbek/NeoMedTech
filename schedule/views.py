from rest_framework import viewsets

from .models import (
    Schedule,
    Appointment,
    TimeSlots,
    WorkDays
)
from .serializers import (
    ScheduleSerializer,
    ScheduleListSerializer,
    AppointmentSerializer,
    AppointmentListSerializer,
    TimeSlotsSerializer,
    WorkDaysSerializer,
    WorkDaysListSerializer
)


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ScheduleListSerializer
        return ScheduleSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AppointmentListSerializer
        return AppointmentSerializer


class TimeSlotsView(viewsets.ModelViewSet):
    serializer_class = TimeSlotsSerializer
    queryset = TimeSlots.objects.all()


class WorkDaysView(viewsets.ModelViewSet):
    serializer_class = WorkDaysSerializer
    queryset = WorkDays.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkDaysListSerializer
        return WorkDaysSerializer
