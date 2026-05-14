from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Doctor(models.Model):  
    name=models.CharField(max_length=50)
    ctry=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    img=models.ImageField(upload_to='doctors') 
    qualfctn=models.CharField(max_length=100,blank=True,null=True)
    
    bio=models.TextField()
    
    def __str__(self):
        return self.name


#Extend User with role
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    ROLE_CHOICES =(

       ('doctor','Doctor'),
       ('patient','Patient'),
       ('admin','Admin')
    )
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.username


    #doctorprofile
class DoctorProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True,blank=True)
    dept=models.CharField(max_length=50)
    qualification=models.CharField(max_length=200,null=True,blank=True)
    experience=models.IntegerField()
    image=models.ImageField(upload_to='doctors',null=True,blank=True)
    def __str__(self):
        return self.user.username


class PatientProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    image=models.ImageField(upload_to='patients',null=True,blank=True)
    GENDER_CHOICES =(
        ('male','Male'),
        ('female','Female')
    )
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
  

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed'),
       
    ]
    patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    doctor=models.ForeignKey(DoctorProfile,on_delete=models.CASCADE)
    phone=models.CharField(max_length=12,null=True,blank=True)
    appointment_date=models.DateField()
    appointment_time=models.TimeField()
    description=models.TextField(null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient.user.username} -  {self.doctor.user.username}"
       
        


class LabReport(models.Model):
    patient=models.ForeignKey('PatientProfile',on_delete=models.CASCADE)
    appointment=models.ForeignKey('Appointment',on_delete=models.CASCADE,null=True,blank=True)
    reportname=models.CharField(max_length=100,null=True,blank=True)
    reportfile=models.FileField(upload_to='labreports')
    uploadedby=models.CharField(max_length=20,
            choices=[
                ('Patient','Patient'),
                ('Lab','Lab')
            ] 
                    )
    uploadedat=models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return self.reportname

class Prescriptions(models.Model):
    appointment = models.OneToOneField('Appointment',on_delete=models.CASCADE)
    doctor=models.ForeignKey('DoctorProfile',on_delete=models.CASCADE)
    patient=models.ForeignKey('PatientProfile',on_delete=models.CASCADE)
    medicines=models.TextField()
    notes=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"""Prescription-{self.patient}"""
