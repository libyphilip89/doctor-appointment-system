from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from django.contrib import  auth
from .forms import *
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from datetime import date,time
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required






# Create your views here.
def homefn(request):
    y=Category.objects.all()
    doctors = Doctor.objects.all()
   
    return render(request,'home.html',{'cat':y,'doctors':doctors})
   
def aboutfn(request):
    return render(request,'about.html')


def doctorsfn(request):
    d=Doctor.objects.all()
    return render(request,'doctors.html',{'doctors':d})
def viewcatfn(request,c_id):  
    a=Doctor.objects.filter(ctry=c_id)    
    return render(request,'doctors.html',{'doctors':a})

def registerfn(request):
    if request.method == 'POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phone']
        password1=request.POST['password1']
        password2=request.POST['password2']
        role=request.POST['role']
        
        if password1 != password2:
                return render(request,'register.html',{'error':'Passwords do not match'})    
        if User.objects.filter(username=username).exists():
                return render(request,'register.html', {'error':'Username already exists'})
            
                #creating user
        user=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password1)
       # creating Userprofile
        UserProfile.objects.create(user=user,phone=phone,role=role)
        return redirect('/login/')
        
          
    return render(request,'register.html')


def loginfn(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
      
        if user:
            auth.login(request,user)
            if user.is_staff:
                return redirect('/admindashboard/')
            try:
                profile=UserProfile.objects.get(user=user)
                
            except UserProfile.DoesNotExist:
                return render(request,'login.html',{'error':'Profile not created'})
                
            if profile.role == 'doctor':
                    if  DoctorProfile.objects.filter(user=user).exists():   
                        return redirect('/doctordashboard/')
                    else:
                         return redirect('/doctorprofile/')

            elif profile.role == 'patient':
                    if PatientProfile.objects.filter(user=user).exists():   
                        return redirect('/patientdashboard/')
                    else:
                        return redirect('/patientprofile/')
            else:
                    return render(request,'login.html',{'error':'invalid role'})   
           
            
           
        else:
          return render(request,"login.html",{'error':'invalid username or password'})
    else:
        return render(request,"login.html")

def logoutfn(request):
    auth.logout(request)
    return redirect('/')
   
@login_required(login_url='/login/')
def doctorprofilefn(request):
    if request.method == 'POST':
        name=request.POST['name']
        dept = request.POST['dept']
        qualification=request.POST['qualification']
        experience=request.POST['experience']
        image=request.FILES['image']

        profile,created = DoctorProfile.objects.get_or_create(user=request.user,name=name,dept=dept,qualification=qualification,
                           experience=experience,image=image)
       
        profile.name = name
        profile.dept = dept
        profile.qualification = qualification
        profile.experience = experience
        profile.image = image
        profile.save()
        return redirect('/doctordashboard/')

    
    return render(request,'doctorprofile.html')
@login_required(login_url='/login/')
def editdoctorprofilefn(request):
    profile = DoctorProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        profile.name=request.POST['name']
        profile.dept = request.POST['dept']
        profile.qualification=request.POST['qualification']
        profile.experience=request.POST['experience']
        profile.save()
        messages.success(request,"Profile updated successfullly")
        return redirect('/doctordashboard/')

       
    return render(request,'editdoctorprofile.html',{'profile':profile})

@login_required(login_url='/login/')
def patientprofilefn(request):
    if request.method == 'POST':

        age = request.POST['age']
        gender = request.POST['gender']
        address=request.POST['address']
        image = request.FILES['image']

        profile,created = PatientProfile.objects.get_or_create(user=request.user)
        profile.name=request.user.first_name
        profile.age = age
        profile.gender = gender
        profile.address = address
        profile.image =image
        profile.save()
        return redirect('/patientdashboard/')
    return render(request,'patientprofile.html')
@login_required(login_url='/login/')
def editpatientprofilefn(request):
    profile = PatientProfile.objects.filter(user=request.user).first()
    if not profile:
        profile = PatientProfile.objects.create(user=request.user)
    if request.method == "POST":
        form=PatientProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile updated successfully")
            return redirect('/patientdashboard/')    
    else:
       
        form=PatientProfileForm(instance=profile)
    return render(request,'editpatientprofile.html',{'fm':form})


@login_required(login_url='/login/')
def doctordashboardfn(request):
    doctor=DoctorProfile.objects.get(user=request.user)
    profile=DoctorProfile.objects.filter(user=request.user)
    today= timezone.now().date()
    
    appointments=Appointment.objects.filter(doctor=doctor)
    today_appointments=appointments.filter(appointment_date=today).exclude(status='Cancelled')
    previous_appointments=appointments.filter(appointment_date__lt=today).exclude(status='Cancelled')
    upcoming_appointments=appointments.filter(appointment_date__gt=today).exclude(status='Cancelled')

    #only reports linked tomthis doctor
    

    
    return render(request,'doctordashboard.html',{'doctor':doctor,'today_appointments':today_appointments,
                                 'upcoming_appointments':upcoming_appointments,'previous_appointments':previous_appointments})

    
    
    


@login_required(login_url='/login/')
def updatestatusfn(request,id):
        appointment=get_object_or_404(Appointment,id=id)
        status= request.GET.get('status')
        if status:
            appointment.status = status
            appointment.save()
        return redirect('/doctordashboard/')

@login_required(login_url='/login/')  
def appointmentdetailfn(request,id):
    appointment=get_object_or_404(Appointment,id=id)
    return render(request,'appointmentdetail.html',{'appointment':appointment})
@login_required(login_url='/login/')
def patientdashboardfn(request):
    patient=PatientProfile.objects.get(user=request.user)
    appointments=Appointment.objects.filter(patient=patient)
     #labreports
    labreports=LabReport.objects.filter(patient=patient).order_by('-uploadedat')
    return render(request,'patientdashboard.html',{'patient':patient,'appointments':appointments,'labreports':labreports})


@staff_member_required(login_url='/login/')
def admindashboardfn(request):
    doctors = Doctor.objects.all()
    patients = PatientProfile.objects.all()
    today_appointments=Appointment.objects.filter(appointment_date=date.today()).exclude(status='Cancelled')
    upcoming_appointments=Appointment.objects.filter(appointment_date__gt=date.today()).exclude(status='Cancelled')
    previous_appointments=Appointment.objects.filter(appointment_date__lt=date.today()).exclude(status='Cancelled')
    return render(request,'admindashboard.html',{'today_appointments':today_appointments,'upcoming_appointments':upcoming_appointments,
          'previous_appointments':previous_appointments})
  
@staff_member_required(login_url='/login/')
def admintodayappointmentsfn(request):
    appointments=Appointment.objects.filter(appointment_date=date.today()).exclude(status='Cancelled')
    return render(request,'admintodayappointments.html',{'appointments':appointments})

@staff_member_required(login_url='/login/')
def adminupcomingappointmentsfn(request):
    appointments=Appointment.objects.filter(appointment_date__gt=date.today()).exclude(status='Cancelled')
    return render(request,'adminupcomingappointments.html',{'appointments':appointments})

@staff_member_required(login_url='/login/')
def adminpreviousappointmentsfn(request):
    appointments=Appointment.objects.filter(appointment_date__lt=date.today()).exclude(status='Cancelled')
    return render(request,'adminpreviousappointments.html',{'appointments':appointments})

@login_required(login_url='/login/')
def updatestatusfn(request,id):
        appointment=get_object_or_404(Appointment,id=id)
        status= request.GET.get('status')
        if status:
            appointment.status = status
            appointment.save()

        if request.user.is_superuser:
            return redirect('/admindashboard/')
        else:

            return redirect('/doctordashboard/')



@login_required(login_url='/login/')
def bookappointmentfn(request):
    patient = PatientProfile.objects.filter(user=request.user).first()
    if not patient:
        messages.error(request,"only patients can book appointment")
        return redirect('/login/')
    form = AppointmentForm()
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']
             #past data validation
            from datetime import date
            if appointment_date < date.today():
                messages.error(request,"Past date booking not allowed")
            elif appointment_time < time(9,0):
                messages.error(request,"No appointment booking before 9AM")
            elif time(13,0) <= appointment_time < time(15,0):
                messages.error(request,"Lunch break.No booking slot available between 1PM to 3PM")
            elif appointment_time > time(18,0):
                messages.error(request,"No appointment booking after 6PM")
            else:
                already_exists = Appointment.objects.filter(doctor=doctor,appointment_date=appointment_date,appointment_time=appointment_time).exists()
                if already_exists:
                    messages.error(request,"This slot is already booked")
                else:
                    appointment = form.save(commit=False)
                    appointment.patient = patient
                    appointment.save()
                    messages.success(request,"Appointment booked successfully")
                    return redirect('/patientdashboard/')
    return render(request,'appointment.html',{'form':form})           

#cancel appointment
@login_required(login_url='/login/')
def cancelappointmentfn(request,id):
    patient=request.user.patientprofile
    appointment =get_object_or_404(Appointment,id=id,patient=patient)
    appointment.status = 'Cancelled'
    appointment.save()
    return redirect('/patientdashboard/')

#reschedule appointment
@login_required(login_url='/login/')
def updateappointmentfn(request,id):
    patient=PatientProfile.objects.filter(user=request.user).first()
    appointment = get_object_or_404(Appointment,id=id,patient=patient)
    form = AppointmentForm(request.POST or None,instance=appointment)
    if request.method == 'POST':
        if form.is_valid():
            doctor=form.cleaned_data['doctor']
            appointment_date=form.cleaned_data['appointment_date']  
            appointment_time=form.cleaned_data['appointment_time'] 
            from datetime import date 
            if appointment_date < date.today():
                messages.error(request,"Past booking is not allowed")

            else:
                already_exists = Appointment.objects.filter(doctor=doctor,appointment_date=appointment_date,
                appointment_time=appointment_time).exclude(id=appointment.id).exists()
                if already_exists:
                    messages.error(request,"This slot is already booked")
                else:
                    form.save()
                    messages.success(request,"Appointment booked successfully")
                    return redirect('/patientdashboard/')
    return render(request,'appointment.html',{'form':form})   
@login_required(login_url='/login/')
def searchfn(request):
    doctor = request.user.doctorprofile
    search = request.GET.get('search')
    appointments =Appointment.objects.filter(doctor=doctor)
    if search:
        appointments = appointments.filter(patient__user__username__icontains=search)
        today_appointments=appointments.filter(appointment_date=date.today())
        upcoming_appointments=appointments.filter(appointment_date__gt=date.today())
        previous_appointments=appointments.filter(appointment_date__lt=date.today())
    return render(request,'doctordashboard.html',{'today_appointments':today_appointments,'upcoming_appointments':upcoming_appointments,'previous_appointments':previous_appointments})

   

@login_required(login_url='/login/')
def labreportsfn(request):
    patient=request.user.patientprofile
    if request.method == 'POST':
        reportname=request.POST.get('reportname')
        reportfile=request.FILES.get('reportfile')
        appointment_id=request.POST.get('appointment')
        appointment=None
        if appointment_id:
            appointment=Appointment.objects.get(id=appointment_id)
        LabReport.objects.create(patient=patient,appointment=appointment,reportname=reportname,reportfile=reportfile,uploadedby='Patient')
        return redirect('/patientdashboard/')

    appointments=Appointment.objects.filter(patient=patient)
    reports = LabReport.objects.filter(patient=patient).order_by('-uploadedat')
    return render(request,'uploadlabreports.html',{'appointments':appointments,'reports':reports})
@login_required(login_url='/login/')
def uploadedlabreportsfn(request):
    patient=request.user.patientprofile
    labreports=LabReport.objects.filter(patient=patient).order_by('-uploadedat')
    return render(request,'uploadedlabreport.html',{'labreports':labreports})
@login_required(login_url='/login/')
def addprescription(request,appointment_id):
    doctor = request.user.doctorprofile
    appointment=Appointment.objects.get(id=appointment_id)
    #prevent duplicate prescriptions
    prescription_exists = Prescriptions.objects.filter(appointment=appointment).exists()
    if prescription_exists:
        return redirect('/doctordashboard/')
    
    if request.method == 'POST':
        medicines=request.POST.get('medicines')
        notes=request.POST.get('notes')
        Prescriptions.objects.create(appointment=appointment,doctor=doctor,
                     patient=appointment.patient,medicines=medicines,notes=notes)
        return redirect('/doctordashboard/')
    return render(request,'addprescription.html',{'appointment':appointment})

@login_required(login_url='/login/')
def patientprescriptionsfn(request):
    patient=request.user.patientprofile
    prescriptions=Prescriptions.objects.filter(patient=patient).order_by('-created_at')
    return render(request,'patientprescription.html',{'prescriptions':prescriptions})

@login_required(login_url='/login/')
def doctorprescriptionsfn(request):
    doctor = request.user.doctorprofile
    prescriptions = Prescriptions.objects.filter(doctor=doctor).order_by('-created_at')
    return render(request,'doctorprescriptions.html',{'prescriptions':prescriptions})
@login_required(login_url='/login/')
def doctorlabreportsfn(request):
    doctor = request.user.doctorprofile
    labreports=LabReport.objects.filter(appointment__doctor=doctor).order_by('-uploadedat')
    return render(request,'doctorlabreport.html',{'labreports':labreports})


@staff_member_required(login_url='/login/')
def adminlabreportfn(request):   
    if request.method == 'POST':
        reportname=request.POST.get('reportname')
        reportfile=request.FILES.get('reportfile')
        appointment_id=request.POST.get('appointment')
        appointment=None
        if appointment_id:
            appointment=Appointment.objects.get(id=appointment_id)
        LabReport.objects.create(patient=appointment.patient,appointment=appointment,reportname=reportname,reportfile=reportfile,uploadedby='Lab')
        return redirect('/admindashboard/')
    appointments=Appointment.objects.all()
    return render(request,'adminuploadlabreport.html',{'appointments':appointments})
    
