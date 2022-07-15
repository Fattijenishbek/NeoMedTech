from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsPatient(BasePermission):

    message = "Sorry but access only for patients"

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == "patient")


class IsDoctor(BasePermission):

    message = "Sorry but access only for doctors"

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == "doctor")


class IsOfficeManager(BasePermission):

    message = "Sorry but access only for office manager"

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == "office_manager")
