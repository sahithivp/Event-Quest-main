from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures\default-avatar.jpeg', blank=True, null=True)
    def __str__(self):
        return self.username
    
class Hall(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)  # Optional
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()  # Duration in hours
    purpose = models.TextField()

    def __str__(self):
        return f"{self.hall.name} booked by {self.name} on {self.date} at {self.time}"

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    purpose = models.TextField()

    def __str__(self):
        return f"Appointment with {self.name} on {self.date} at {self.time}"