from django.contrib import admin
from .models import RawData, ExcelData
from django.contrib.auth.models import User, Group


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_valid')
    readonly_fields = ('id',)


@admin.register(ExcelData)
class ExcelDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_valid')
    readonly_fields = ('id',)


admin.site.unregister(User)
admin.site.unregister(Group)
