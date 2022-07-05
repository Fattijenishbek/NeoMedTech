from xml.etree.ElementInclude import include
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from rest_framework.routers import DefaultRouter
from . import views


router1 = DefaultRouter()

router1.register(r'answer', views.AnswerView)
router1.register(r'question', views.QuestionView)
router1.register(r'med-card', views.MedCardView)
router1.register(r'check-list', views.CheckListView)

urlpatterns = [
    path('', include(router1.urls))
]