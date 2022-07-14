from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import UserViewSet, PatientViewSet, DoctorViewSet, OfficeManagerViewSet
user_router = DefaultRouter()
user_router.register(r'all-users', UserViewSet, basename='all-users')
user_router.register(r'patient', PatientViewSet, basename='patient')
user_router.register(r'doctor', DoctorViewSet, basename='doctor')
user_router.register(r'office-manager', OfficeManagerViewSet, basename='office-manager')
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("register_patient/", views.RegisterPatientView.as_view()),
    path("login/", views.LoginWebView.as_view()),
    path("login_mob/", views.LoginMobileView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]