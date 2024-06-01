from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import transac_search
from .views import  approve_alumni_request,claim_alumni_id
urlpatterns = [
    path('', views.home, name="home"),
    path('requestgmc', views.requestgmc, name="requestgmc"),
    path('equipmenttracker', views.equipmentTracker, name='equipmentTracker'),
    path('equipmenttrackerAdmin/', views.equipmentTrackerAdmin, name='equipmentTrackerAdmin'),
    path('adminmain', views.adminhome, name="adminmain"),
    path('requested-gmc', views.adminRequestedGmc, name='adminRequestedGmc'),
    path('gmc-form', views.gmcform, name="gmcform"),
    path('generate-gmc/<int:request_id>/', views.generateGmc, name='generateGmc'),
    path('monthlyCalendar', views.monthlyCalendar, name='monthlyCalendar'),
    path('monthlyCalendarAdmin', views.monthlyCalendarAdmin, name='monthlyCalendarAdmin'),
    path('save-schedule/', views.save_schedule, name='save_schedule'),
    path('delete-schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('addEquipment/', views.addEquipment, name='addEquipment'),

    path('id_request/',views.idRequest, name="idRequest"),
    path('search_id/', views.search_id, name='search_id'),
    path('add_alumni/', views.add_alumni, name="add_alumni"),
    path('search_id2/', views.search_id2, name='search_id2'),
    path('graduateTracer_submit', views.graduateTracer_submit,name='graduateTracer_submit'),
    path('graduatetracer/',views.graduateTracer, name="graduateTracer"),
    path('reunionandevents/',views.alumni_events, name="alumni_events"),
    path('jobfairs/',views.jobfairs, name="jobfairs"),
    path('yearbook/',views.yearbook, name="yearbook"),
    path('search_yearbook/', views.search_yearbook, name='search_yearbook'),
    path('transaction_alumni.html/',views.transaction_alumni, name="transaction_alumni"),
    path('transac_search', transac_search, name='transac_search'),
    path('admin_id_request/', views.admin_id_request, name='admin_idRequest'),
    path('approve_alumni_request/<int:alumni_id>/', approve_alumni_request, name='approve_alumni_request'),
    path('claim_alumni_id/<int:alumni_id>/', claim_alumni_id, name='claim_alumni_id'),
    path('admin_grad_tracer/', views.admin_gradTracer, name='admin_gradTracer'),
    path('admin_events/', views.admin_events, name='admin_events'),    
    path('admin_jobfairs',views.admin_jobfairs, name="admin_jobfairs"),
    path('admin_yearbook',views.admin_yearbook, name="admin_yearbook"),





]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
