from django.shortcuts import redirect, render
from django.contrib import messages  # Import messages modul
from .models import studentInfo, RequestedGMC
from django.utils.timezone import localtime, now

# Create your views here.

def home(request):
    return render(request, "studentLife/main.html")

def adminhome(request):
    return render(request, "adminUser/adminmain.html")

def adminGmc(request):
    return render(request, "adminUser/adminRequestedGmc.html")

def gmcform(request):
    return render(request, "adminUser/gmcform.html")

def requestgmc(request):
    student = None

    if request.method == "GET" and "searchID" in request.GET:
        student_id = request.GET.get("searchID")
        if student_id:
            try:
                student = studentInfo.objects.get(studID=student_id)
            except studentInfo.DoesNotExist:
                student = None
                messages.error(request, "Student not found")

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        reason = request.POST.get("reason")
        if student_id and reason:
            try:
                student = studentInfo.objects.get(studID=student_id)
                RequestedGMC.objects.create(student=student, reason=reason)
                messages.success(request, "Good Moral Certificate request submitted successfully")
                return redirect('requestgmc') 
            except studentInfo.DoesNotExist:
                messages.error(request, "Student not found")

    context = {"student": student}
    return render(request, "studentLife/requestgmc.html", context)

def adminRequestedGmc(request):
    gmc_requests = RequestedGMC.objects.filter(processed=False)
    context = {"gmc_requests": gmc_requests}
    return render(request, "adminUser/adminRequestedGmc.html", context)


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
    
def monthlyCalendar(request):
    return render(request, "studentLife/monthlyCalendar.html")


def monthlyCalendarAdmin(request):
    return render(request, 'adminUser/monthlyCalendarAdmin.html')

