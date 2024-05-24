from django.contrib import admin
from .models import studentInfo,RequestedGMC,Schedule

# Register your models here.

admin.site.register(studentInfo)
admin.site.register(RequestedGMC)
admin.site.register(Schedule)