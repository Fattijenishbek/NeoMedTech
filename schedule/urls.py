from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ScheduleViewSet,
    AppointmentViewSet,
    TimeSlotsView,
    GetFreeTimeViewSet,
    HolidayViewSet,
    AppointmentOfDoctorForWeekViewSet,
    GetDoctorScheduleForOneDayViewSet,
)

schedule_router = DefaultRouter()

schedule_router.register(r'schedule', ScheduleViewSet, basename='schedule')
schedule_router.register(r'appointment', AppointmentViewSet, basename='appointment')
schedule_router.register(r'time-slots', TimeSlotsView, basename='time-slots')
schedule_router.register(r'get-free-time', GetFreeTimeViewSet, basename='get-free-time')
schedule_router.register(r'schedule-with-appointment', AppointmentOfDoctorForWeekViewSet,
                         basename='schedule-with-appointment')
schedule_router.register(r'get-doctors-schedule-for-one-day', GetDoctorScheduleForOneDayViewSet,
                         basename='get-doctors-schedule-for-one-day')
schedule_router.register(r'holidays', HolidayViewSet, basename='holidays')
urlpatterns = [
    path('', include(schedule_router.urls))
]
