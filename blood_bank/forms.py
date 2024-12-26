from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Donor, Recipient, BloodGroup, Profile
import re

# -------------------------
# Custom User Creation Form
# -------------------------

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    
    # Adding custom styling for fields
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2


# -------------------------
# Donor Form (Updated with Location)
# -------------------------

class DonorForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Donor Name'})
    )
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Age'}))
    contact = forms.CharField(
        max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Contact Number'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 4, 'cols': 40})
    )
    location = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Location'})
    )

    class Meta:
        model = Donor
        fields = ['name', 'age', 'blood_group', 'contact', 'address', 'location']

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        # Regex to check for a valid phone number format (can be adjusted to your specific format)
        if not re.match(r'^\+?\d{10,15}$', contact):
            raise forms.ValidationError("Please enter a valid contact number.")
        return contact
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError("Donor must be at least 18 years old.")
        return age

    def clean_blood_group(self):
        blood_group = self.cleaned_data.get('blood_group')
        if not blood_group:
            raise forms.ValidationError("Please select a blood group.")
        return blood_group


# -------------------------
# Recipient Form (Updated with Location)
# -------------------------

class RecipientForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Recipient Name'})
    )
    contact = forms.CharField(
        max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Contact Number'})
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Reason for Blood Request', 'rows': 4, 'cols': 40})
    )
    location = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Location'})
    )
    
    blood_group = forms.ModelChoiceField(queryset=BloodGroup.objects.all(), empty_label='Select Blood Group')

    class Meta:
        model = Recipient
        fields = ['name', 'blood_group', 'contact', 'reason', 'location']

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        # Regex to check for a valid phone number format (can be adjusted to your specific format)
        if not re.match(r'^\+?\d{10,15}$', contact):
            raise forms.ValidationError("Please enter a valid contact number.")
        return contact
    
    def clean_reason(self):
        reason = self.cleaned_data.get('reason')
        if not reason:
            raise forms.ValidationError("Please provide a reason for the blood request.")
        return reason


# -------------------------
# Profile Form (Updated)
# -------------------------

class ProfileForm(forms.ModelForm):
    location = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Location'})
    )
    blood_group = forms.ModelChoiceField(queryset=BloodGroup.objects.all(), empty_label='Select Blood Group')
    phone_number = forms.CharField(
        max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )

    class Meta:
        model = Profile
        fields = ['location', 'blood_group', 'phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Regex to check for valid phone number format
        if not re.match(r'^\+?\d{10,15}$', phone_number):
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone_number


# -------------------------
# Custom User Creation Form
# -------------------------

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  
        if commit:
            user.save()
        return user
    
    #donor2 form for registration
   
from django import forms
from .models import DonorReg

class DonorRegForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    last_donation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    class Meta:
        model = DonorReg
        fields = [
            'username', 'full_name', 'dob', 'gender', 'phone', 'email', 'dob',
            'address', 'blood_group', 'health_confirmed', 'emergency_donor', 'preferred_times','last_donation_date', 'password'
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'preferred_times': forms.TextInput(attrs={'placeholder': 'Specify preferred times (Morning, Afternoon, Evening)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data
    
    
    #donor2 form new for login
    
    
# # forms.py
# from django import forms
# from .models import DonorReg

# class DonorLoginForm(forms.Form):
#     username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
#         'placeholder': 'Enter your username',
#         'class': 'form-control',
#     }))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'placeholder': 'Enter your password',
#         'class': 'form-control',
#     }))

#     def clean(self):
#         cleaned_data = super().clean()
#         username = cleaned_data.get('username')
#         password = cleaned_data.get('password')

#         if username and password:
#             try:
#                 donor = DonorReg.objects.get(username=username)
#                 if donor.password != password:  # Simple check (Use hashing in production)
#                     raise forms.ValidationError("Invalid password.")
#             except DonorReg.DoesNotExist:
#                 raise forms.ValidationError("Donor with this username does not exist.")
#         return cleaned_data


from django import forms
from .models import DonorReg

class DonorLoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'form-control',
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                donor = DonorReg.objects.get(username=username)
                if donor.password != password:  # Simple check (Use hashing in production)
                    raise forms.ValidationError("Invalid password.")
            except DonorReg.DoesNotExist:
                raise forms.ValidationError("Donor with this username does not exist.")
        return cleaned_data