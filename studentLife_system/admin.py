from django.contrib import admin
from .models import studentInfo,RequestedGMC,Schedule

class StudentInfoAdmin(admin.ModelAdmin):
    
    list_display = ('studID', 'lastname', 'firstname', 'middlename', 'degree', 'yearlvl', 'sex', 'emailadd', 'contact')
    search_fields = ('studID', 'lastname', 'firstname', 'lrn')
    list_filter = ('degree', 'yearlvl', 'sex')

admin.site.register(studentInfo, StudentInfoAdmin)

class requestedgmcAdmin(admin.ModelAdmin):
    list_display = ('student', 'reason', 'or_num', 'request_date', 'processed')

admin.site.register(RequestedGMC, requestedgmcAdmin)


class scheduleAdmin(admin.ModelAdmin):
    list_display = ('sched_Id','title', 'description', 'start_datetime', 'end_datetime')

admin.site.register(Schedule, scheduleAdmin)