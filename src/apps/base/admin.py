from django.contrib import admin
from apps.base import models

# Register your models here.
admin.site.register(models.Licensing)
admin.site.register(models.Plan)
admin.site.register(models.Profile)
