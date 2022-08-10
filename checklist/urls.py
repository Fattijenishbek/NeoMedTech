from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
# from .views import MedcardDetailView, MedcardView

checklist_router = DefaultRouter()

checklist_router.register(r'question', views.QuestionView, basename='question')
checklist_router.register(r'answer', views.AnswerView, basename='answer')
checklist_router.register(r'title', views.TitleView, basename='title')
checklist_router.register(r'med-card', views.MedCardView, basename='med-card')
checklist_router.register(r'check-list', views.CheckListView, basename='check-list')
# path("medcard/<int:patient>", MedcardDetailView.as_view(), name='products'),
#     path("medcard", MedcardView.as_view(), name='product-category'),

urlpatterns = [
    path('', include(checklist_router.urls)),
    # path("medcard/<int:pk>", views.MedcardDetailView.as_view(), name='products'),
    # path("medcard", views.MedcardView.as_view(), name='product-category'),
]
