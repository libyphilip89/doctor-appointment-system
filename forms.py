from django import forms
from.models import *


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['name','age','gender','address','image']

        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter  name'

            }),
            'age':forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Enter age'

            }),
            'gender':forms.Select(attrs={
                'class':'form-select',
                'placeholder':'Enter your gender'

            }),
            'address':forms.Textarea(attrs={
                'class':'form-control',
                'rows':3,
                'placeholder':'Enter address'

            }),
            'image':forms.ClearableFileInput(attrs={
                'class':'form-control',
               

            }),



        }


def clean(self):
    cleaned_data = super().clean()
    start = cleaned_data.get('start_time')
    end = cleaned_data.get('end_time')
    if start and end and start >= end:
        raise forms.validationError("End time must be after start time")
        return cleaned_data

        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model=Appointment
        fields=['doctor','phone','appointment_date','appointment_time','description']
        widgets ={
            'doctor':forms.Select(attrs={'class':'form-control'}),

            
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter phonenumber'}),
            'appointment_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'appointment_time':forms.Select(attrs={'class':'form-control'}),
            
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Describe your problem',
                'rows':3}),
           
        }

#phone validation
def clean_phone(self):
    phone=self.cleaned_data.get('phone')
    if not phone.isdigit():
        raise forms.validationError("Enter valid phone number")
    if len(phone) < 10:
        raise forms.validationError("Phone number must be at least 10 digits")
    return phone
