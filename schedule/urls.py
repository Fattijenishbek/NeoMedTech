from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ScheduleViewSet,
    AppointmentViewSet,
    TimeSlotsView,
    GetFreeTimeViewSet,
    HolidayViewSet
)

schedule_router = DefaultRouter()

schedule_router.register(r'schedule', ScheduleViewSet, basename='schedule')
schedule_router.register(r'appointment', AppointmentViewSet, basename='appointment')
schedule_router.register(r'time-slots', TimeSlotsView, basename='time-slots')
schedule_router.register(r'get-free-time', GetFreeTimeViewSet, basename='get-free-time')
schedule_router.register(r'holidays', HolidayViewSet, basename='holidays')
urlpatterns = [
    path('', include(schedule_router.urls))
]
