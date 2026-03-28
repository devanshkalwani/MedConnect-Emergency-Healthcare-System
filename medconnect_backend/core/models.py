from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# USER MODEL
# =========================
class User(AbstractUser):

    name = models.CharField(max_length=200, blank=True, default="")

    email = models.EmailField(unique=True)

    contact_number = models.CharField(max_length=15)

    blood_group = models.CharField(max_length=5)
    age = models.PositiveIntegerField(null=True, blank=True)

    allergies = models.TextField(blank=True)
    medical_condition = models.TextField(blank=True)
    pref_contact = models.CharField(max_length=100, blank=True, default="")
    pref_hospital = models.CharField(max_length=150, blank=True, default="")

    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)

    is_hospital = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# =========================
# HOSPITAL MODEL
# =========================
class Hospital(models.Model):

    name = models.CharField(max_length=200)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    total_beds = models.IntegerField()
    icu_beds = models.IntegerField()

    # 📍 Location (future real GPS use)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # 🔥 DEMO PURPOSE (distance in KM from patient)
    distance = models.FloatField(default=0)

    def __str__(self):
        return self.name


# =========================
# SOS REQUEST MODEL
# =========================
class SOSRequest(models.Model):

    STATUS_CHOICES = [
        ('SEARCHING', 'Searching'),
        ('ASSIGNED', 'Assigned'),
        ('RESOLVED', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    emergency_type = models.CharField(max_length=200)

    # 🔥 NEW: V2.0 Third-Party Victim Reporting
    is_for_self = models.BooleanField(default=True)
    third_party_name = models.CharField(max_length=150, null=True, blank=True)
    third_party_phone = models.CharField(max_length=20, null=True, blank=True)
    third_party_condition = models.TextField(null=True, blank=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SEARCHING')

    assigned_hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # 🔥 IMPORTANT (for radius logic)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOS {self.id} - {self.user.name}"


class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"