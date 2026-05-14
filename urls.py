"""
URL configuration for Dctr_appoinment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static

from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homefn),
    path('about/', aboutfn),
    path('register/', registerfn),
    path('login/', loginfn),
    path('logout/', logoutfn),

    path('doctors/', doctorsfn),
    path('viewcat/<int:c_id>/', viewcatfn,name='viewcat'),
    path('doctorprofile/', doctorprofilefn),
    path('editdoctorprofile/', editdoctorprofilefn),
    path('patientprofile/', patientprofilefn),
    path('editpatientprofile/', editpatientprofilefn),
    path('patientdashboard/', patientdashboardfn),
    path('doctordashboard/', doctordashboardfn),
    path('search/', searchfn),    
    path('bookappointment/', bookappointmentfn),
    path('updateappointment/<int:id>/', updateappointmentfn),
    path('cancelappointment/<int:id>/', cancelappointmentfn),
    path('appointmentdetail/<int:id>/', appointmentdetailfn),
    path('updatestatus/<int:id>/', updatestatusfn),
    path('labreports/', labreportsfn),
    path('uploadedlab/',uploadedlabreportsfn),
    path('patientprescriptions/',patientprescriptionsfn),
    path('addprescriptions/<int:appointment_id>/',addprescription),
    path('doctorlabreports/',doctorlabreportsfn),
    path('doctorprescriptions/',doctorprescriptionsfn),
    path('admindashboard/',admindashboardfn),  
    path('todayappointments/',admintodayappointmentsfn),
    path('upcomingappointments/',adminupcomingappointmentsfn), 
    path('previousappointments/',adminpreviousappointmentsfn), 
    path('adminuploadlabreport/',adminlabreportfn),
   

    
    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


