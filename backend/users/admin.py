from django.contrib import admin
from .models import User


@admin.register(User)
class WellLocationAdmin(admin.ModelAdmin):
    list_display=['username','email','role','iroha_name']