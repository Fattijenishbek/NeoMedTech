from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views
from .views import (
    UserViewSet,
    OfficeManagerViewSet,
    DoctorProfileViewSet,
    PatientProfileViewSet,
    PasswordResetView,
    PasswordResetConfirmView,
    PatientProfileSortingViewSet,
    PatientViewSet,
)

user_router = DefaultRouter()
user_router.register(r'all-users', UserViewSet, basename='all-users')
user_router.register(r'office-manager', OfficeManagerViewSet, basename='office-manager')
user_router.register(r'doctor-profile', DoctorProfileViewSet, basename='doctor-profile')
user_router.register(r'patient-profile', PatientProfileViewSet, basename='patient-profile')
user_router.register(r'patient', PatientViewSet, basename='patient')
user_router.register(r'patient2', PatientProfileSortingViewSet, basename='patient2')

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("register_patient/", views.RegisterPatientView.as_view()),
    path("login/", views.LoginWebView.as_view()),
    path("login_mob/", views.LoginMobileView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
