from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages  
from .models import studentInfo, RequestedGMC,equipment,Schedule
from django.utils.timezone import localtime, now
from .forms import ScheduleForm
from datetime import datetime
from .models import Alumni,graduateForm,Event,JobFair,Yearbook
from django.utils import timezone
from django.db.models import Avg
import json
from django.core.mail import send_mail,BadHeaderError
import socket
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

def idRequest(request):
    return render(request, 'alumni/users/id_alumni.html')


def search_id(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        if student_id:
            try:
                student_obj = studentInfo.objects.get(studID=student_id)
                return render(request, 'alumni/users/id_alumni.html', {'student': student_obj})
            except studentInfo.DoesNotExist:
                
                messages.error(request, 'No student found with the provided ID.')
                return render(request, 'alumni/users/id_alumni.html')
        else:
            
            messages.error(request, 'Please provide a student ID.')
            return render(request, 'alumni/users/id_alumni.html')
    else:
        
        return render(request, 'alumni/users/id_alumni.html')
    

def add_alumni(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        email_add = request.POST.get('email_add')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        alumnidate = request.POST.get('alumnidate')
        alumnibirthday = request.POST.get('alumnibirthday')
        alumnicontact = request.POST.get('alumnicontact')
        sssgsis = request.POST.get('sssgsis')
        tin = request.POST.get('tin')
        parentguardian = request.POST.get('parentguardian')
        alumniaddress = request.POST.get('alumniaddress')
        degree = request.POST.get('degree')
        sex = request.POST.get('sex')
        
        if Alumni.objects.filter(student__studID=student_id).exists():
            messages.error(request, f'You already requested Alumni ID!')
            return redirect('idRequest')

        student = get_object_or_404(studentInfo, studID=student_id)
        alumni = Alumni.objects.create(student=student, firstname=firstname, lastname=lastname,
                               alumnidate=alumnidate, alumnibirthday=alumnibirthday,
                               alumnicontact=alumnicontact, sssgsis=sssgsis, tin=tin,
                               parentguardian=parentguardian, alumniaddress=alumniaddress,email_add=email_add,degree=degree,sex=sex)
        alumni_id = alumni.alumniID
        
        messages.success(request, f'Your request is successful! Your alumni ID requested is {alumni_id}')
        
        return redirect('idRequest')
    else:
        return redirect('idRequest')    
    

def graduateTracer(request):
    return render(request, 'alumni/users/graduateTracer.html')

def search_id2(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        if student_id:
            try:
                
                alumni_obj = Alumni.objects.get(student__studID=student_id)
                
                
                if graduateForm.objects.filter(student__studID=student_id).exists():
                    messages.error(request, 'You have already filled out this form.')
                    return render(request, 'alumni/users/graduateTracer.html')
                
                return render(request, 'alumni/users/graduateTracer.html', {'alumni': alumni_obj})
            except Alumni.DoesNotExist:
                messages.error(request, 'Not Found! Please request first for alumni ID')
                return render(request, 'alumni/users/graduateTracer.html')
        else:
            messages.error(request, 'Please provide a student ID.')
            return render(request, 'alumni/users/graduateTracer.html')
    else:
        return render(request, 'alumni/users/graduateTracer.html')
    
def graduateTracer_submit(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        degree = request.POST.get('degree')
        email_add = request.POST.get('email_add')
        contactnum = request.POST.get('contactnum')
        sex = request.POST.get('sex')
        alumniaddress = request.POST.get('alumniaddress')
        dategraduated = request.POST.get('dategraduated')
        nameoforganization = request.POST.get('nameoforganization')
        employmenttype = request.POST.get('employmentype')
        occupationalClass = request.POST.get('occupationalClass')
        gradscholrelated = request.POST.get('gradscholrelated')
        yearscompany = request.POST.get('yearscompany')
        placework = request.POST.get('placework')
        firstjobgraduate = request.POST.get('firstjobgraduate')
        reasonstayingjob = request.POST.get('reasonstayingjob')
        designation = request.POST.get('designation')
        status = request.POST.get('status')
        monthlyincome = request.POST.get('monthlyincome')
        workwhileworking = request.POST.get('workwhileworking')
        ifnotworking = request.POST.get('ifnotworking')
        reasontimegap = request.POST.get('reasontimegap')
        natureemployment = request.POST.get('natureemployment')
        numberofyears = request.POST.get('numberofyears')
        monthlyincome2 = request.POST.get('monthlyincome2')
        academicprofession = request.POST.get('academicprofession')
        researchcapability = request.POST.get('researchcapability')
        learningefficiency = request.POST.get('learningefficiency')
        peopleskills = request.POST.get('peopleskills')
        problemsolvingskills = request.POST.get('problemsolvingskills')
        informationtechnologyskills = request.POST.get('informationtechnologyskills')
        meetingprofessionalneeds = request.POST.get('meetingprofessionalneeds')
        communityfield = request.POST.get('communityfield')
        globalfield = request.POST.get('globalfield')
        criticalskills = request.POST.get('criticalskills')
        rangeofcourses = request.POST.get('rangeofcourses')
        relevanceprofession = request.POST.get('relevanceprofession')
        extracurricular = request.POST.get('extracurricular')
        premiumresearch = request.POST.get('premiumresearch')
        interlearning = request.POST.get('interlearning')
        teachingenvironment = request.POST.get('teachingenvironment')
        qualityinstruction = request.POST.get('qualityinstruction')
        teachrelationship = request.POST.get('teachrelationship')
        libraryresources = request.POST.get('libraryresources')
        labresources = request.POST.get('labresources')
        classize = request.POST.get('classize')
        profexpertise = request.POST.get('profexpertise')
        profsubjectmatter = request.POST.get('profsubjectmatter')
        enrollmentdate = request.POST.get('enrollmentdate')
        studiesdegree = request.POST.get('studiesdegree')
        universityinstitution = request.POST.get('universityinstitution')
        studiesAddress = request.POST.get('studiesAddress')
        pursuingstudies = request.POST.get('pursuingstudies')  
        department = request.POST.get('department')  
        salaryimprovement = request.POST.get('salaryimprovement')  
        opportunitiesabroad = request.POST.get('opportunitiesabroad')  
        personalitydevelopment = request.POST.get('personalitydevelopment')  
        technologiesvaluesformation = request.POST.get('technologiesvaluesformation')  
        try:
            student = get_object_or_404(studentInfo, studID=student_id)
        except:
            messages.error(request, 'Student ID not found.')
            return redirect('graduateTracer')

        try:
            alumni = get_object_or_404(Alumni, student=student)
        except:
            messages.error(request, 'No Alumni matches the given query.')
            return redirect('graduateTracer')
        gradform = graduateForm.objects.create( alumniID=alumni,student=student,
                                    degree=degree,
                                    email_add=email_add,
                                    contactnum=contactnum,
                                    sex=sex,
                                    firstname=firstname,
                                    lastname=lastname,
                                    alumniaddress=alumniaddress,
                                    dategraduated=dategraduated,
                                    nameoforganization=nameoforganization,
                                    employmenttype=employmenttype,
                                    occupationalClass=occupationalClass,
                                    gradscholrelated=gradscholrelated,
                                    yearscompany=yearscompany,
                                    placework=placework,
                                    firstjobgraduate=firstjobgraduate,
                                    reasonstayingjob=reasonstayingjob,
                                    designation=designation,
                                    status=status,
                                    monthlyincome=monthlyincome,
                                    workwhileworking=workwhileworking,
                                    ifnotworking=ifnotworking,
                                    reasontimegap=reasontimegap,
                                    numberofyears=numberofyears,
                                    monthlyincome2=monthlyincome2,
                                    academicprofession=academicprofession,
                                    researchcapability=researchcapability,
                                    learningefficiency=learningefficiency,
                                    peopleskills=peopleskills,
                                    problemsolvingskills=problemsolvingskills,
                                    informationtechnologyskills=informationtechnologyskills,
                                    communityfield=communityfield,
                                    globalfield=globalfield,
                                    criticalskills=criticalskills,
                                    rangeofcourses=rangeofcourses,
                                    relevanceprofession=relevanceprofession,
                                    extracurricular=extracurricular,
                                    premiumresearch=premiumresearch,
                                    interlearning=interlearning,
                                    teachingenvironment=teachingenvironment,
                                    qualityinstruction=qualityinstruction,
                                    teachrelationship=teachrelationship,
                                    libraryresources=libraryresources,
                                    labresources=labresources,
                                    classize=classize,
                                    profexpertise=profexpertise,
                                    profsubjectmatter=profsubjectmatter,
                                    enrollmentdate=enrollmentdate,
                                    studiesdegree=studiesdegree,
                                    universityinstitution=universityinstitution,
                                    studiesAddress=studiesAddress,
                                    pursuingstudies=pursuingstudies,
                                    department=department,
                                    natureemployment = natureemployment,
                                    meetingprofessionalneeds=meetingprofessionalneeds,
                                    salaryimprovement=salaryimprovement,
                                    opportunitiesabroad=opportunitiesabroad,
                                    personalitydevelopment=personalitydevelopment,
                                    technologiesvaluesformation=technologiesvaluesformation,
                                    
    )
        alumni_id = alumni.alumniID
        
        messages.success(request, f'Your request is successful! Your alumni ID is {alumni_id}')
        return redirect('graduateTracer')
    else:
        return redirect('graduateTracer')    
    
def alumni_events(request):
    events = Event.objects.all()    
    return render(request, 'alumni/users/alumni_events.html', {'events': events})    


def jobfairs(request):

    job_fairs = JobFair.objects.all()
    return render(request, 'alumni/users/jobfairs.html', {'job_fairs': job_fairs})


def yearbook(request):
    return render(request, 'alumni/users/yearbook.html')


def search_yearbook(request):
    if request.method == 'GET':
        first_name = request.GET.get('yeargetfirstname')
        last_name = request.GET.get('yeargetlastname')

        if first_name and last_name:
            try:
               
                first_name = first_name.lower()
                last_name = last_name.lower()

       
                yearbook_entry = Yearbook.objects.get(yearbookFirstname__iexact=first_name, yearbookLastname__iexact=last_name)
                return render(request, 'alumni/users/yearbook.html', {'yearbook_entry': yearbook_entry})
            except Yearbook.DoesNotExist:
                return render(request, 'alumni/users/yearbook.html', {'error_message': 'No yearbook entry found.'})
        else:
            return render(request, 'alumni/users/yearbook.html', {'error_message': 'Please provide both first name and last name in the search.'})
    else:
        return render(request, 'alumni/users/yearbook.html')


def transaction_alumni(request):
    return render(request, 'alumni/users/transaction_alumni.html')

def transac_search(request):
    context = {}
    
    if request.method == 'POST':
        transac_choice = request.POST.get('transac_choice')
        transac_frequency = request.POST.get('transac_frequency')

        current_month = timezone.now().month

        # Alumni ID Requests
        if transac_choice == 'Alumni ID Requests':
            if transac_frequency == 'Monthly':
                alumni_requests = Alumni.objects.filter(alumnidate__month=current_month)
            elif transac_frequency == 'Yearly':
                alumni_requests = Alumni.objects.filter(alumnidate__year=timezone.now().year)
            else:
                alumni_requests = Alumni.objects.all()

            total_count = alumni_requests.count()
            context = {
                'alumni_requests': alumni_requests,
                'transac_frequency': transac_frequency,
                'total_count': total_count,
                'transac_choice': transac_choice
            }

        # Graduate Tracer
        elif transac_choice == 'Graduate Tracer':
            if transac_frequency == 'Monthly':
                graduate_tracer_data = graduateForm.objects.filter(enrollmentdate__month=current_month)
            elif transac_frequency == 'Yearly':
                graduate_tracer_data = graduateForm.objects.filter(enrollmentdate__year=timezone.now().year)
            else:
                graduate_tracer_data = graduateForm.objects.all()

            total_count = graduate_tracer_data.count()
            has_reports = total_count > 0

            # Aggregate weighted means
            weighted_means = {
                'academicprofession': graduate_tracer_data.aggregate(Avg('academicprofession'))['academicprofession__avg'],
                'researchcapability': graduate_tracer_data.aggregate(Avg('researchcapability'))['researchcapability__avg'],
                'learningefficiency': graduate_tracer_data.aggregate(Avg('learningefficiency'))['learningefficiency__avg'],
                'peopleskills': graduate_tracer_data.aggregate(Avg('peopleskills'))['peopleskills__avg'],
                'problemsolvingskills': graduate_tracer_data.aggregate(Avg('problemsolvingskills'))['problemsolvingskills__avg'],
                'informationtechnologyskills': graduate_tracer_data.aggregate(Avg('informationtechnologyskills'))['informationtechnologyskills__avg'],
                'meetingprofessionalneeds': graduate_tracer_data.aggregate(Avg('meetingprofessionalneeds'))['meetingprofessionalneeds__avg'],
                'communityfield': graduate_tracer_data.aggregate(Avg('communityfield'))['communityfield__avg'],
                'globalfield': graduate_tracer_data.aggregate(Avg('globalfield'))['globalfield__avg'],
                'criticalskills': graduate_tracer_data.aggregate(Avg('criticalskills'))['criticalskills__avg'],
                'salaryimprovement': graduate_tracer_data.aggregate(Avg('salaryimprovement'))['salaryimprovement__avg'],
                'opportunitiesabroad': graduate_tracer_data.aggregate(Avg('opportunitiesabroad'))['opportunitiesabroad__avg'],
                'personalitydevelopment': graduate_tracer_data.aggregate(Avg('personalitydevelopment'))['personalitydevelopment__avg'],
                'technologiesvaluesformation': graduate_tracer_data.aggregate(Avg('technologiesvaluesformation'))['technologiesvaluesformation__avg'],
                'rangeofcourses': graduate_tracer_data.aggregate(Avg('rangeofcourses'))['rangeofcourses__avg'],
                'relevanceprofession': graduate_tracer_data.aggregate(Avg('relevanceprofession'))['relevanceprofession__avg'],
                'extracurricular': graduate_tracer_data.aggregate(Avg('extracurricular'))['extracurricular__avg'],
                'premiumresearch': graduate_tracer_data.aggregate(Avg('premiumresearch'))['premiumresearch__avg'],
                'interlearning': graduate_tracer_data.aggregate(Avg('interlearning'))['interlearning__avg'],
                'teachingenvironment': graduate_tracer_data.aggregate(Avg('teachingenvironment'))['teachingenvironment__avg'],
                'qualityinstruction': graduate_tracer_data.aggregate(Avg('qualityinstruction'))['qualityinstruction__avg'],
                'teachrelationship': graduate_tracer_data.aggregate(Avg('teachrelationship'))['teachrelationship__avg'],
                'libraryresources': graduate_tracer_data.aggregate(Avg('libraryresources'))['libraryresources__avg'],
                'labresources': graduate_tracer_data.aggregate(Avg('labresources'))['labresources__avg'],
                'classize': graduate_tracer_data.aggregate(Avg('classize'))['classize__avg'],
                'profexpertise': graduate_tracer_data.aggregate(Avg('profexpertise'))['profexpertise__avg'],
                'profsubjectmatter': graduate_tracer_data.aggregate(Avg('profsubjectmatter'))['profsubjectmatter__avg']
            }

            context = {
                'graduate_tracer_data': graduate_tracer_data,
                'transac_frequency': transac_frequency,
                'total_count': total_count,
                'transac_choice': transac_choice,
                'weighted_means': weighted_means,
                'has_reports': has_reports
            }

    return render(request, 'alumni/users/transaction_alumni.html', context)


# admin alumni
def admin_id_request(request):
    alumni_requests = Alumni.objects.all()
    return render(request, 'alumni/users/admin_idRequest.html', {'alumni_requests': alumni_requests})

def approve_alumni_request(request, alumni_id):
    if request.method == 'POST':
        alumni = get_object_or_404(Alumni, pk=alumni_id)
        email_add = alumni.email_add

        try:
            send_mail(
                'Alumni ID Request Approved',
                f'Hello {alumni.firstname} {alumni.lastname},\n\nYour alumni ID request has been approved. Your ID is ready to claim.\n\nThank you!',
                'alumni_ctuac@ctu.edu.ph',
                [email_add],
                fail_silently=False,
            )
            alumni.approved = True  # Mark as approved
            alumni.save()

        except (socket.error, BadHeaderError) as e:
            messages.error(request, f'Error sending email: {e}')
        
        return redirect('admin_idRequest')

    return redirect('admin_idRequest')
    
def claim_alumni_id(request, alumni_id):
    if request.method == 'POST':
        alumni = get_object_or_404(Alumni, pk=alumni_id)
        alumni.claimed_date = timezone.now()
        alumni.save()
        return redirect('admin_idRequest')

    return redirect('admin_idRequest')

def admin_gradTracer(request):
    graduate_requests = graduateForm.objects.select_related('alumniID').all()
    return render(request, 'alumni/users/admin_gradTracer.html', {'graduate_requests': graduate_requests})

def admin_events(request):
    if request.method == 'POST':
        
        eventsName = request.POST.get('eventsName')
        eventsDate = request.POST.get('eventsDate')
        eventsLocation = request.POST.get('eventsLocation')
        eventsDescription = request.POST.get('eventsDescription')
        eventsImage = request.FILES.get('eventsImage') 

        
        event = Event.objects.create(
            eventsName=eventsName,
            eventsDate=eventsDate,
            eventsLocation=eventsLocation,
            eventsDescription=eventsDescription,
            eventsImage=eventsImage
        )
        messages.success(request, 'Successfully Added!')
        
        return redirect('admin_events')

    return render(request, 'alumni/users/admin_events.html')



def admin_jobfairs(request):
    if request.method == 'POST':

        jobtitle = request.POST.get('jobtitle')
        companyname = request.POST.get('companyname')
        joblocation = request.POST.get('joblocation')
        jobsalary = request.POST.get('jobsalary')
        employmenttype = request.POST.get('employmenttype')
        jobdescription = request.POST.get('jobdescription')


        
        jobfair = JobFair.objects.create(
            jobtitle=jobtitle,
            companyname=companyname,
            joblocation=joblocation,
            jobsalary=jobsalary,
            employmenttype=employmenttype,
            jobdescription=jobdescription
        )

        messages.success(request, 'Successfully Added!')
        return redirect('admin_jobfairs')

    return render(request, 'alumni/users/admin_jobfairs.html')


def admin_yearbook(request):
    if request.method == 'POST':
        yearbookFirstname = request.POST.get('yearfirstname')
        yearbookLastname = request.POST.get('yearlastname')
        yearbookAddress = request.POST.get('yearaddress')
        yearbookCourse = request.POST.get('yearcourse')
        yearbookImage = request.FILES.get('yearImage')  
        yearbookGender = request.POST.get('yeargender')
        yearbookYearGrad = request.POST.get('yeargraduated')

        # Check if an entry with the same first name and last name already exists
        if Yearbook.objects.filter(yearbookFirstname=yearbookFirstname, yearbookLastname=yearbookLastname).exists():
            messages.error(request, 'An entry with this name already exists.')
        else:
            yearbook_entry = Yearbook.objects.create(
                yearbookFirstname=yearbookFirstname,
                yearbookLastname=yearbookLastname,
                yearbookAddress=yearbookAddress,
                yearbookCourse=yearbookCourse,
                yearbookImage=yearbookImage,
                yearbookGender=yearbookGender,
                yearbookYearGrad=yearbookYearGrad
            )
            messages.success(request, 'Successfully Added!')
        
        return redirect('admin_yearbook')

    return render(request, 'alumni/users/admin_yearbook.html')