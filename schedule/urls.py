from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ScheduleViewSet,
    AppointmentViewSet,
    WorkDateViewSet,
)

schedule_router = DefaultRouter()

schedule_router.register(r'schedule', ScheduleViewSet)
schedule_router.register(r'appointment', AppointmentViewSet)
schedule_router.register(r'work-date', WorkDateViewSet)

urlpatterns = [
    path('', include(schedule_router.urls))
]
