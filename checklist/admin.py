from django.contrib import admin

from .models import *
for i in [CheckList, MedCard, Title, Question, Answer]:
    admin.site.register(i)