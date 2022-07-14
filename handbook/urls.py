from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from rest_framework.routers import DefaultRouter

from .views import *

handbook_router = DefaultRouter()

handbook_router.register(r'handbook', HandBookViewSet)
handbook_router.register(r'todo', TodoViewSet)
handbook_router.register(r'essentials', EssentialsViewSet)
handbook_router.register(r'article', ArticleViewSet)
handbook_router.register(r'pictures', PicturesViewSet)


urlpatterns = [
    path('', include(handbook_router.urls))
]
