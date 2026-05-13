import uuid
from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('employee', 'Bank Employee'),
    ('customer', 'Customer'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def is_admin(self):
        return self.role == 'admin'

    def is_employee(self):
        return self.role == 'employee'

    def is_customer(self):
        return self.role == 'customer'
