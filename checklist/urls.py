from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

checklist_router = DefaultRouter()

checklist_router.register(r'answer', views.AnswerView)
checklist_router.register(r'question', views.QuestionView)
checklist_router.register(r'med-card', views.MedCardView)
checklist_router.register(r'check-list', views.CheckListView)

urlpatterns = [
    path('', include(checklist_router.urls))
]
