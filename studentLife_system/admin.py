from django.contrib import admin
from .models import studentInfo,RequestedGMC,Schedule,equipment
from .models import Alumni,graduateForm,Event,Yearbook,Event,JobFair
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

class AlumniAdmin(admin.ModelAdmin):
    list_display = ('alumniID', 'student_id', 'firstname','lastname','degree','alumniaddress')

    def get_firstname(self, obj):
        return obj.student.fname
    get_firstname.short_description = 'First Name'

    def get_lastname(self, obj):
        return obj.student.lname
    get_lastname.short_description = 'Last Name'


class graduateFormAdmin(admin.ModelAdmin):
    list_display = ('get_alumniID', 'dategraduated', 'firstname', 'lastname', 'alumniaddress')

    def get_alumniID(self, obj):
        return obj.alumniID.alumniID
    get_alumniID.short_description = 'Alumni ID'
class EventAdmin(admin.ModelAdmin):
    list_display = ('eventID', 'eventsName', 'eventsDate', 'eventsLocation')

class JobFairAdmin(admin.ModelAdmin):
    list_display = ('jobfair_id', 'jobtitle','companyname', 'joblocation','employmenttype','jobsalary')
class YearbookAdmin(admin.ModelAdmin):
    list_display = ('yearbookID','yearbookFirstname', 'yearbookLastname', 'yearbookGender', 'yearbookAddress', 'yearbookCourse' ,'yearbookYearGrad')

    
admin.site.register(Yearbook, YearbookAdmin)
admin.site.register(JobFair, JobFairAdmin)    
admin.site.register(Event, EventAdmin)       
admin.site.register(graduateForm, graduateFormAdmin)
admin.site.register(Alumni, AlumniAdmin)
admin.site.register(Schedule, scheduleAdmin)

admin.site.register(equipment)


