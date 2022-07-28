from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

checklist_router = DefaultRouter()

checklist_router.register(r'option', views.OptionView, basename='option')
checklist_router.register(r'question', views.QuestionView, basename='question')
checklist_router.register(r'med-card', views.MedCardView, basename='med-card')
checklist_router.register(r'check-list', views.CheckListView, basename='check-list')
checklist_router.register(r'check', views.CheckView, basename='check')


urlpatterns = [
    path('', include(checklist_router.urls))
]
