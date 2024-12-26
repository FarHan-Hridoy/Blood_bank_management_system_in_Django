import os
import django

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_bank_project.settings')
django.setup()

# Import necessary models
from blood_bank.models import User, Profile

# Fetch the user
username = 'Muhtasim007'
user = User.objects.get(username=username)

# Check if the profile already exists
profile, created = Profile.objects.get_or_create(
    user=user,  # Use user object
    defaults={
        'blood_type': None,  # Default values if creating a new profile
        'phone_number': '01303074462',
        'address': 'Test Address',
        'location': 'Chashma Hill',
    }
)

if created:
    print(f"Profile created for user: {user.username}")
else:
    print(f"Profile already exists for user: {user.username}")