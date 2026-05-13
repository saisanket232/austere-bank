import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_bank.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

employees = UserProfile.objects.filter(role__in=['admin', 'employee'])
for profile in employees:
    print(f"Username: {profile.user.username}, Role: {profile.role}")

if not employees.exists():
    print("No employee/admin users found.")
