from xml.etree.ElementInclude import include
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register(r'answer', views.AnswerView)
router.register(r'question', views.QuestionView)
router.register(r'med-card', views.MedCardView)
router.register(r'check-list', views.CheckListView)

urlpatterns = [
    path('', include(router.urls))
]