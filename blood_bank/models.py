from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta
# from blood_bank.models import Profile, User

# -------------------------
# Blood Group Model
# -------------------------
class BloodGroup(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name="Blood Group")

    class Meta:
        verbose_name = "Blood Group"
        verbose_name_plural = "Blood Groups"

    def __str__(self):
        return self.name


# -------------------------
# Donor Model
# -------------------------
class Donor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="donor", null=True, blank=True
    )
    birth_date = models.DateField(verbose_name="Date of Birth")
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.PROTECT)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number.")],
        verbose_name="Phone Number",
        default="0000000000"
    )
    address = models.TextField(verbose_name="Address")
    location = models.CharField(max_length=100, null=True, blank=True)
    last_donated_date = models.DateField(null=True, blank=True)
    donation_date = models.DateField(null=True, blank=True, verbose_name="Last Donation Date")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Donor"
        verbose_name_plural = "Donors"
        ordering = ["-donation_date"]

    def age(self):
        today = date.today()
        return (
            today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def is_eligible_for_donation(self):
        return self.age() >= 18 and (self.donation_date is None or (date.today() - self.donation_date).days >= 90)

    def clean(self):
        if self.age() < 18:
            raise ValidationError("Donors must be at least 18 years old.")
        if self.age() > 65:
            raise ValidationError("Donors cannot be older than 65 years.")
        
    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.blood_group.name}"


# -------------------------
# Recipient Model
# -------------------------
class Recipient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recipient")
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    birth_date = models.DateField(verbose_name="Date of Birth")  # Changed 'dob' to 'birth_date'
    contact = models.CharField(max_length=15, verbose_name="Contact Information")
    medical_conditions = models.TextField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    medications = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    nid_number = models.CharField(
        max_length=10,
        verbose_name="NID Number",
        validators=[RegexValidator(r'^\d{10}$', "Enter a valid 10-digit NID number.")],
    )
    nid_image = models.ImageField(upload_to="nid_images/", null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number.")]
    )
    consent = models.BooleanField(default=False)
    signature = models.CharField(max_length=255)
    needed_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recipient"
        verbose_name_plural = "Recipients"
        ordering = ["-created_at"]

    def clean(self):
        if self.needed_date and self.needed_date < date.today():
            raise ValidationError("The needed date cannot be in the past.")
    
    def __str__(self):
        return f"{self.full_name} ({self.blood_group.name})"

    def is_urgent(self):
        return self.needed_date and self.needed_date <= date.today() + timedelta(days=3)


# -------------------------
# Profile Model
# -------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number.")],
        blank=True,
        verbose_name="Phone Number",
        default="0000000000"  
    )
    address = models.TextField(verbose_name="Address", default="Unknown")  # Fixed redundancy
    location = models.CharField(max_length=100, null=True, blank=True, default="Unknown")
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"


# -------------------------
# Signals to Manage Profiles
# -------------------------
@receiver(post_save, sender=User)
def manage_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
        
        
        
        

# -------------------------
# Recipient Model backup
# -------------------------
class Recipient2(models.Model):
    
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recipient")
    username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name="Date of Birth")  # Changed 'dob' to 'birth_date'
    address = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    nid_number = models.CharField(max_length=20, null=True, blank=True)
    by_date = models.DateField(null=True, blank=True)
    units = models.PositiveIntegerField(default=1)  # New field for units
    # action
    
    
    #for new user profile updated version
    


class Recipient2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, unique=False)
    username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    blood_group = models.ForeignKey('BloodGroup', on_delete=models.CASCADE)
    
    birth_date = models.DateField()
    address = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    nid_number = models.CharField(max_length=20, null=True, blank=True)
    by_date = models.DateField(null=True, blank=True)
  
  
  #Inventory Newly Added

from django.db import models

class BloodInventory(models.Model):
    blood_type = models.CharField(max_length=3)  # e.g., A+, O-
    units = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.blood_type

#New status feature action button

class Recipient2(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name="Date of Birth")
    address = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    nid_number = models.CharField(max_length=20, null=True, blank=True)
    by_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Add this field
    units = models.PositiveIntegerField(default=1)  # Ensure this field exists

    def __str__(self):
        return f"{self.username} - {self.status}"
    
    
    #new donor
    # models.py
from django.contrib.auth.hashers import make_password, check_password

class DonorReg(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    health_confirmed = models.BooleanField(default=False)
    emergency_donor = models.BooleanField(default=False)
    preferred_times = models.TextField(blank=True, null=True)
    last_donation_date = models.DateField(verbose_name="Last Donation Date", blank=True, null=True)  # Added field
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Add this field

    def __str__(self):
        return self.username

