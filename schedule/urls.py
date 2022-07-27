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

schedule_router.register(r'schedule', ScheduleViewSet)
schedule_router.register(r'appointment', AppointmentViewSet)
schedule_router.register(r'time-slots', TimeSlotsView)
schedule_router.register(r'get-free-time', GetFreeTimeViewSet)
schedule_router.register(r'holidays', HolidayViewSet)
urlpatterns = [
    path('', include(schedule_router.urls))
]
