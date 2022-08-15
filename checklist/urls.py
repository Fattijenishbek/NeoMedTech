from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

checklist_router = DefaultRouter()

checklist_router.register(r'question', views.QuestionView, basename='question')
checklist_router.register(r'answer', views.AnswerView, basename='answer')
checklist_router.register(r'title', views.TitleView, basename='title')
checklist_router.register(r'med-card', views.MedCardView, basename='med-card')
checklist_router.register(r'med-card-archive', views.ArchiveMedCardView, basename='med-card-archive')
checklist_router.register(r'check-list', views.CheckListView, basename='check-list')
checklist_router.register(r'check-list-archive', views.ArchiveCheckListView, basename='check-list-archive')
checklist_router.register(r'checklist-template', views.CheckListTemplateView, basename='checklist-template')


urlpatterns = [
    path('', include(checklist_router.urls))
]
