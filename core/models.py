from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]
    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('resting', 'Resting'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    weight = models.FloatField()
    medical_notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='active')
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.blood_type})"


class BloodInventory(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, unique=True)
    units_available = models.IntegerField(default=0)
    minimum_threshold = models.IntegerField(default=10)
    last_updated = models.DateTimeField(auto_now=True)

    def is_critical(self):
        return self.units_available < self.minimum_threshold

    def __str__(self):
        return f"{self.blood_type} - {self.units_available} units"


class BloodRequest(models.Model):
    PRIORITY = [
        ('critical', 'Critical'),
        ('urgent', 'Urgent'),
        ('normal', 'Normal'),
    ]
    STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('fulfilled', 'Fulfilled'),
        ('rejected', 'Rejected'),
    ]

    requester_name = models.CharField(max_length=100)
    hospital = models.CharField(max_length=200)
    blood_type = models.CharField(max_length=3)
    units_needed = models.IntegerField()
    priority = models.CharField(max_length=10, choices=PRIORITY, default='normal')
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    notes = models.TextField(blank=True)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hospital} - {self.blood_type} ({self.units_needed} units)"


class DonationRecord(models.Model):
    TYPES = [
        ('donation', 'Donation'),
        ('issued', 'Issued'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True, blank=True)
    blood_type = models.CharField(max_length=3)
    units = models.IntegerField(default=1)
    transaction_type = models.CharField(max_length=10, choices=TYPES)
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.blood_type} ({self.units} units)"
