from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or
                    request.user and request.user.is_superuser)


class IsPatientOrOfficeManager(BasePermission):
    message = 'Permission denied'
    edit_methods = ["DELETE"]

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS
                    or request.user and request.user.user_type == "patient"
                    and request.method not in self.edit_methods
                    or request.user.user_type == 'office_manager')


class IsSuperUserOrOfficeManager(BasePermission):
    message = 'Permission denied'

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or
                    request.user and request.user.user_type == 'office_manager' or
                    request.user and request.user.is_superuser)


class IsSuperUserOrOfficeManagerOrDoctor(BasePermission):
    message = 'Permission denied'

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.user_type == 'office_manager' or
                    request.user and request.user.is_superuser or
                    request.user and request.user.user_type == 'doctor')


class IsPatientOrIsDoctor(BasePermission):
    message = 'Permission denied'

    edit_methods = ["DELETE", ]

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or
                    request.user and request.user.user_type == 'patient'
                    and request.method not in self.edit_methods or
                    request.user and request.user.user_type == 'office_manager' or
                    request.user and request.user.user_type == 'doctor'
                    and request.method not in self.edit_methods)
