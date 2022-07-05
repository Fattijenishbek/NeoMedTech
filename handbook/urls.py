from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'handbook', HandBookViewSet),
router.register(r'todo', TodoViewSet),
router.register(r'essentials', EssentialsViewSet)

urlpatterns = [
    path('', include(router.urls))
]