from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages  
from .models import studentInfo, RequestedGMC,equipment,Schedule
from django.utils.timezone import localtime, now
from .forms import ScheduleForm
from datetime import datetime
import json

# Create your views here.

# Student 
def home(request):
    return render(request, "studentLife/main.html")

# Admin
def adminhome(request):
    return render(request, "adminUser/adminmain.html")

def adminGmc(request):
    return render(request, "adminUser/adminRequestedGmc.html")

def gmcform(request):
    return render(request, "adminUser/gmcform.html")

def equipmentTracker(request):
    return render(request, "studentLife/equipmentTracker.html")

# Request for GoodMoral Certificate Student Side 
def requestgmc(request):
    student = None

    if request.method == "GET" and "searchID" in request.GET:
        student_id = request.GET.get("searchID")
        if student_id:
            if student_id.isdigit():
                try:
                    student = studentInfo.objects.get(studID=student_id)
                except studentInfo.DoesNotExist:
                    student = None
                    messages.error(request, "Student not found")
            else:
                messages.error(request, "Student ID must be numeric")

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        reason = request.POST.get("reason")
        if student_id and reason:
            if student_id.isdigit():
                try:
                    student = studentInfo.objects.get(studID=student_id)
                    RequestedGMC.objects.create(student=student, reason=reason)
                    messages.success(request, "Good Moral Certificate request submitted successfully")
                    return redirect('requestgmc') 
                except studentInfo.DoesNotExist:
                    messages.error(request, "Student not found")
            else:
                messages.error(request, "Student ID must be numeric")

    context = {"student": student}
    return render(request, "studentLife/requestgmc.html", context)

# Processing Goodmoral Certificate Admin side 
def adminRequestedGmc(request):
    gmc_requests = RequestedGMC.objects.filter(processed=False)
    context = {"gmc_requests": gmc_requests}
    return render(request, "adminUser/adminRequestedGmc.html", context)

# Making of Goodmoral Certificate
def generateGmc(request, request_id):
    try:
        gmc_request = RequestedGMC.objects.get(id=request_id)
        student = gmc_request.student
        or_num = request.GET.get('ornum', '')  # Capture the OR Number from the query parameters

        # Mark the request as processed
        gmc_request.or_num = or_num
        gmc_request.processed = True
        gmc_request.save()

        context = {
            "student_name": f"{student.firstname} {student.lastname}",
            "student_degree": student.degree,
            "request_date": localtime(gmc_request.request_date).strftime('%B %d, %Y'),
            "reason": gmc_request.reason,
            "today_date": localtime(now()).strftime('%B %d, %Y'),
            "or_num": or_num  # Include the OR Number in the context
        }
        return render(request, "adminUser/good_moral_certificate.html", context)
    except RequestedGMC.DoesNotExist:
        messages.error(request, "GMC Request not found")
        return redirect('adminRequestedGmc')

# Calendar Of Activities Student Side 
def monthlyCalendar(request):
    schedules = Schedule.objects.all()
    sched_res = {}

    for schedule in schedules:
        sched_res[schedule.sched_Id] = {
            'id': schedule.sched_Id,
            'title': schedule.title,
            'description': schedule.description,
            'start_datetime': schedule.start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            'end_datetime': schedule.end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            'sdate': schedule.start_datetime.strftime("%B %d, %Y %I:%M %p"),
            'edate': schedule.end_datetime.strftime("%B %d, %Y %I:%M %p")
        }

    context = {
        'sched_json': json.dumps(sched_res)
    }
    return render(request, "studentLife/monthlyCalendar.html", context)

# Calendar of Activities Admin 
def monthlyCalendarAdmin(request):
    schedules = Schedule.objects.all()
    sched_res = {}

    for schedule in schedules:
        sched_res[schedule.sched_Id] = {
            'id': schedule.sched_Id,
            'title': schedule.title,
            'description': schedule.description,
            'start_datetime': schedule.start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            'end_datetime': schedule.end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            'sdate': schedule.start_datetime.strftime("%B %d, %Y %I:%M %p"),
            'edate': schedule.end_datetime.strftime("%B %d, %Y %I:%M %p")
        }

    context = {
        'sched_json': json.dumps(sched_res)
    }
    return render(request, 'adminUser/monthlyCalendarAdmin.html', context)


# Save Schedule
def save_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('id')
        if schedule_id:
            schedule = get_object_or_404(Schedule, pk=schedule_id)
            form = ScheduleForm(request.POST, instance=schedule)
        else:
            form = ScheduleForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('monthlyCalendarAdmin')
    else:
        form = ScheduleForm()
    return render(request, 'adminUser/monthlyCalendarAdmin.html', {'form': form})

# Delete Schedule
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    schedule.delete()
    return redirect('monthlyCalendarAdmin')


def equipmentTrackerAdmin(request):
    student = None

    if request.method == "GET" and "search" in request.GET:
        search_id = request.GET.get("search")
        if search_id:
            try:
                student = studentInfo.objects.get(studID=search_id)
            except studentInfo.DoesNotExist:
                messages.error(request, "Student not found")

    all_equipment = equipment.objects.all()

    context = {
        'student': student,
        'all_equipment': all_equipment
    }
    return render(request, 'adminUser/equipmentTrackerAdmin.html', context)


# Add Equipment
def addEquipment(request):
    if request.method == "POST":
        equipment_name = request.POST.get("equipmentname")
        serial = request.POST.get("serialnum")
        
        if equipment_name:
            new_equipment = equipment(equipmentName=equipment_name, equipmentSN=serial)
            new_equipment.save()
            messages.success(request, "Equipment added successfully")
            return redirect('addEquipment')
        else:
            messages.error(request, "Both fields are required")

    # Fetch all equipment objects from the database
    all_equipment = equipment.objects.all()

    # Pass the equipment objects to the template context
    return render(request, 'adminUser/addEquipment.html', {'all_equipment': all_equipment})

