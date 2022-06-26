from django.contrib import admin
from .models import (
    User,
    Patient,
    Doctor,
)


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "phone", "username", "user_type", "email", 'password', "birth_date", "is_staff", "is_superuser",
                    "is_active"]
    list_display_links = ['phone']
    list_editable = ["is_staff", "is_superuser", "is_active"]


admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
