from django.contrib import admin

# Register your models here.
from coordinates.models import Coordinates


@admin.register(Coordinates)
class CoordinatesAdmin(admin.ModelAdmin):
    pass
