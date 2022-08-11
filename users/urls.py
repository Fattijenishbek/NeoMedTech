from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)
from rest_auth.views import (
    PasswordResetView, PasswordResetConfirmView
)
from . import views
from .views import (
    AdminViewSet,
    OfficeManagerViewSet,
    DoctorViewSet,
    PatientViewSet,
    RegisterDoctorView,
    PersonalLoginWebView,
    LoginMobileView,
)

user_router = DefaultRouter()
user_router.register(r'admins', AdminViewSet, basename='admins')
user_router.register(r'office-manager', OfficeManagerViewSet, basename='office-manager')
user_router.register(r'doctor', DoctorViewSet, basename='doctor')
user_router.register(r'patient', PatientViewSet, basename='patient')

urlpatterns = [
    path("register/doctor/", RegisterDoctorView.as_view()),
    path("register/patient/", views.RegisterPatientView.as_view()),
    path("register/office-manager/", views.RegisterOfficeManagerView.as_view()),
    path("login/personal/", PersonalLoginWebView.as_view()),
    path("login/mob/", LoginMobileView.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path("refresh/", TokenRefreshView.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('jwt/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('jwt/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('jwt/token/verify',
         TokenVerifyView.as_view(),
         name='token_verify'),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("confirm-email/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="confirm-email"),
]
