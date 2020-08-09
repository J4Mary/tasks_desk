from django.contrib import admin

# Register your models here.
from . import models


class Admin(admin.ModelAdmin):
    list_display = ['id', 'text', 'status', 'created_by', 'assigned_to']
    list_editable = ['text', 'status', 'assigned_to']


admin.site.register(models.Card, Admin)

