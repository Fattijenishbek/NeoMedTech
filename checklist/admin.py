from django.contrib import admin

from .models import (
    CheckList,
    Option,
    Title,
    MedCard,
)


admin.site.register(CheckList)
admin.site.register(Title)
admin.site.register(Option)