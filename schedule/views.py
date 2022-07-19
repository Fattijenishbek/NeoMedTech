from rest_framework import viewsets

from .models import (
    Schedule,
    Appointment,
    WorkDate,
)
from .serializers import (
    ScheduleSerializer,
    AppointmentSerializer,
    WorkDateSerializer,
)


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()


class WorkDateViewSet(viewsets.ModelViewSet):
    serializer_class = WorkDateSerializer
    queryset = WorkDate.objects.all()
