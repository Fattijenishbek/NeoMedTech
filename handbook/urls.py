from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from rest_framework.routers import DefaultRouter

from .views import *

router2 = DefaultRouter()

router2.register(r'handbook', HandBookViewSet),
router2.register(r'todo', TodoViewSet),
router2.register(r'essentials', EssentialsViewSet)
router2.register(r'article', ArticleViewSet)

urlpatterns = [
    path('', include(router2.urls))
]