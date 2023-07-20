"""models file """
import random

import django
from django.contrib.auth.models import User
from djongo import models


# Create your models here.

GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
)


class Appointment(models.Model):
    """Appointment Model"""
    patient_id = models.IntegerField(default=0)
    date = models.DateField(default=django.utils.timezone.now)
    name = models.CharField(default="unknown", max_length=30)
    time = models.TimeField(default=django.utils.timezone.now, blank=True, null=True)


class Food(models.Model):
    """Food Model"""
    patient_id = models.IntegerField(default=0)
    Name = models.CharField(max_length=50)
    number = models.IntegerField(default=1)
    max_Cholesterol = models.IntegerField(default=150)
    max_Liver_function = models.IntegerField(default=55)
    max_Kidney_function = models.IntegerField(default=60)
    max_Blood_Pressure = models.IntegerField(default=80)
    pic = models.ImageField(upload_to='profile_pic/Food/', null=True, blank=True)


class FoodPatient(models.Model):
    """FoodPatient Model"""
    patient_id = models.IntegerField(default=0)
    foodName = models.CharField(max_length=50)


# BSPM2022T1
class Medication(models.Model):
    """Medication Model"""
    patient_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    numOftimes = models.PositiveIntegerField(default=0)
    mg = models.PositiveIntegerField(default=0)
    expiratDate = models.CharField(max_length=50)
    Description = models.CharField(max_length=3000)


class Feedback(models.Model):
    """Feedback Model"""
    sen_id = models.IntegerField(default=0)
    rec_id = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    by = models.CharField(max_length=40)
    message = models.CharField(max_length=500)
    senderType = models.CharField(max_length=40, default="user type")
    replay = models.CharField(max_length=500, default="There is no response to this message")


class Patient(models.Model):
    """Patient Model"""
    id = models.IntegerField(default=random.randint(0,10000), primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    age = models.IntegerField(default=15)
    symptoms = models.CharField(max_length=100, null=True)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    profile_pic = models.ImageField(upload_to='profile_pic/PatientProfilePic/',
                                    null=True, blank=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    Urine_surgery = models.CharField(max_length=1000, default='u')
    Blood_Pressure = models.IntegerField(default=80)
    Glucose = models.IntegerField(default=80)
    Fats = models.IntegerField(default=20)
    Cholesterol = models.IntegerField(default=150)
    Liver_function = models.IntegerField(default=55)
    Kidney_function = models.IntegerField(default=60)
    ECG = models.IntegerField(default=70)



class Record(models.Model):
    """Record Model"""
    nurse_id = models.IntegerField(default=0)
    patientName = models.CharField(max_length=40)
    body = models.CharField(max_length=500)


class Nurse(models.Model):
    """Nurse Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, default='Cardiologist')
    profile_pic = models.ImageField(upload_to='profile_pic/NurseProfilePic/', null=True, blank=True)
    status = models.BooleanField(default=False)
