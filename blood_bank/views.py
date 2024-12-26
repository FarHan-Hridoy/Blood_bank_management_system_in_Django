from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.views import LoginView
from .models import Donor, Recipient,Recipient2, Profile, BloodGroup, DonorReg
from django.http import HttpResponse
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from .forms import DonorForm, RecipientForm, ProfileForm
from blood_bank.models import Recipient2
import logging

# Set up logging
logger = logging.getLogger(__name__)

# -------------------------
# Utility Functions
# -------------------------

def search_queryset(model, query, search_fields):
    """
    Generic function to filter objects based on query and specified fields.
    """
    if not query:
        return model.objects.all()
    filters = Q()
    for field in search_fields:
        filters |= Q(**{f"{field}__icontains": query})
    return model.objects.filter(filters).distinct()

# -------------------------
# Authentication Views
# -------------------------

class CustomLoginView(LoginView):
    """
    Custom login view to redirect users to their profile upon successful login.
    """
    def get_success_url(self):
        return reverse('blood_bank:profile')

def register(request):
    if request.method == 'POST':
        by_date = request.POST.get('by_date', '').strip() #new added by me 
        units = request.POST.get('units', '1')  # Get the units field, default to 1
        # Collect form data
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()
        location = request.POST.get('location', '').strip()
        blood_type_id = request.POST.get('blood_type')
        phone_number = request.POST.get('phone_number', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        dob = request.POST.get('dob', '').strip()
        nid_number = request.POST.get('nid_number', '').strip()
        

        # Validate form data
        if not username or not password or not confirm_password:
            messages.error(request, "Username and password fields are required.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken!')
            return redirect('register')

        if not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, 'Please enter a valid phone number with 10 digits.')
            return redirect('register')

        # Validate blood group selection
        blood_group = BloodGroup.objects.filter(id=blood_type_id).first()
        if blood_type_id and not blood_group:
            messages.error(request, 'Invalid blood group selected.')
            return redirect('register')

        # Validate Date of Birth (DOB)
        try:
            blood_group = BloodGroup.objects.get(id=blood_type_id)  # Fetch the valid BloodGroup
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            by_date_obj = datetime.strptime(by_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Please enter a valid date of birth in the format YYYY-MM-DD.')
            return redirect('blood_bank:register')

        # Create the user and recipient
        try:
            # Create the user
            
            
            print("hi2")
            ns = Recipient2(username=username,
                full_name=full_name,
                birth_date=dob_date,
                blood_group=blood_group,
                address=location,
                contact=phone_number,
                nid_number=nid_number,
                by_date=by_date_obj,  # Save By Date
                units=int(units),
                )
            print(ns)
            ns.save()
            print("hi4")
            print("hi")
            user = User.objects.create_user(username = username, password= password)
            # Create the Recipient object
            # Recipient.objects.create(
                # user=user,
                # full_name=full_name,
                # dob=dob_date,
                # contact=phone_number,
                # blood_group=blood_group,
                # nid_number=nid_number,
                # address=location,
            # )
            

            # Log the user in after successful registration
            login(request, user)
            return redirect('blood_bank:profile')

            # Success message
            messages.success(request, 'Registration successful! You are now registered as a recipient.')

            # Redirect to profile page or another page
            return redirect('blood_bank:profile')  # Adjust the redirection to wherever you want

        except Exception as e:
            messages.error(request, f'Error during registration: {e}')
            return redirect('register')

    else:
        # Handle GET requests: render the registration form
        blood_groups = BloodGroup.objects.all()  # Fetch blood groups for the dropdown
        return render(request, 'registration/register.html', {'blood_groups': blood_groups})
# -------------------------
# Profile Views
# -------------------------

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from blood_bank.models import Recipient2
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from blood_bank.models import Recipient2
from django.http import HttpResponse

@login_required
def profile(request):
    print(f"User: {request.user}")  # Debugging to check the current user
    try:
        recipient = request.user.recipient2_profile  # Assuming a relationship exists
        print(f"Recipient: {recipient}")  # Debugging recipient data
    except Recipient2.DoesNotExist:
        recipient = None
        print("No recipient profile found.")
        
    return render(request, 'profile.html', {'recipient': recipient})

@login_required
def profile(request):
    try:
        # Fetch the Recipient2 object linked to the logged-in user
        #  = request.user.recipient2_profile
        recipient = Recipient2.objects.filter(username = request.user.username).first()
        return render(request, 'profile.html', {'recipient': recipient})
    except Recipient2.DoesNotExist:
        # Handle the case where no recipient is linked to the user
        return HttpResponse("No recipient data found for this user.")

@login_required
def logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    """
    logout(request)  # Logs out the current user
    return redirect('/login/') 
    

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
# from blood_bank.models import Recipient2
# from django.http import HttpResponse

# @login_required
# def profile(request):
#     print(f"User: {request.user}")  # Debugging to check the current user
#     try:
#         recipient = Recipient2.objects.filter(username=request.user.username).first()
#         print(f"Recipient: {recipient}")  # Debugging recipient data
#     except Recipient2.DoesNotExist:
#         recipient = None
#         print("No recipient profile found.")
        
#     return render(request, 'profile.html', {'recipient': recipient})

# @login_required
# def logout_view(request):
#     """
#     Logs out the current user and redirects to the login page.
#     """
#     logout(request)  # Logs out the current user
#     return redirect('/login/')  # Redirects to the login page
    
    

@login_required
def profile_edit(request):
    """
    Allows users to update their profile information.
    """
    profile = get_object_or_404(Profile, user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('blood_bank:profile')

    return render(request, 'profile_edit.html', {'form': form})

# -------------------------
# Home View
# -------------------------

def home(request):
    """
    Displays the home page.
    """
    return render(request, 'home.html')

# -------------------------
# Donor Management Views
# -------------------------

@login_required
def donor_list(request):
    """
    Displays a searchable list of donors.
    """
    query = request.GET.get('q', '')
    donors = search_queryset(Donor, query, ['user__username', 'blood_group__name', 'location']).select_related('blood_group', 'user')
    return render(request, 'donor_list.html', {'donors': donors, 'query': query})

@login_required
def create_donor(request):
    """
    Allows users to create a donor profile.
    """
    form = DonorForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Donor added successfully!')
        return redirect('blood_bank:donor_list')

    return render(request, 'create_donor.html', {'form': form})

@login_required
def edit_donor(request, id):
    """
    Allows users to edit donor details.
    """
    donor = get_object_or_404(Donor, id=id)

    if donor.user != request.user:
        messages.error(request, "You don't have permission to edit this donor.")
        return redirect('blood_bank:donor_list')

    form = DonorForm(request.POST or None, instance=donor)

    if form.is_valid():
        form.save()
        messages.success(request, 'Donor updated successfully!')
        return redirect('blood_bank:donor_list')

    return render(request, 'edit_donor.html', {'form': form, 'donor': donor})

@login_required
def delete_donor(request, id):
    """
    Allows users to delete donor profiles.
    """
    donor = get_object_or_404(Donor, id=id)

    if donor.user != request.user:
        messages.error(request, "You don't have permission to delete this donor.")
        return redirect('blood_bank:donor_list')

    if request.method == 'POST':
        donor.delete()
        messages.success(request, 'Donor deleted successfully!')
        return redirect('blood_bank:donor_list')

    return render(request, 'delete_donor.html', {'donor': donor})

# -------------------------
# Recipient Management Views
# -------------------------

@login_required
def recipient_list(request):
    """
    Displays a searchable list of recipients.
    """
    query = request.GET.get('q', '')
    recipients = search_queryset(Recipient, query, ['user__username', 'blood_group__name', 'address']).prefetch_related('user', 'blood_group')
    return render(request, 'recipient_list.html', {'recipients': recipients, 'query': query})

@login_required
def create_recipient(request):
    if request.method == 'POST':
        # Handle form submission
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipient created successfully!")
            return redirect('some_view_name')
    else:
        form = RecipientForm()
    
    return render(request, 'blood/create_recipient.html', {'form': form})

@login_required
def edit_recipient(request, id):
    """
    Allows users to edit recipient details.
    """
    recipient = get_object_or_404(Recipient, id=id)

    if recipient.user != request.user:
        messages.error(request, "You don't have permission to edit this recipient.")
        return redirect('blood_bank:recipient_list')

    form = RecipientForm(request.POST or None, instance=recipient)

    if form.is_valid():
        form.save()
        messages.success(request, 'Recipient updated successfully!')
        return redirect('blood_bank:recipient_list')

    return render(request, 'edit_recipient.html', {'form': form, 'recipient': recipient})

@login_required
def delete_recipient(request, id):
    """
    Allows users to delete recipient profiles.
    """
    recipient = get_object_or_404(Recipient, id=id)

    if recipient.user != request.user:
        messages.error(request, "You don't have permission to delete this recipient.")
        return redirect('blood_bank:recipient_list')

    if request.method == 'POST':
        recipient.delete()
        messages.success(request, 'Recipient deleted successfully!')
        return redirect('blood_bank:recipient_list')

    return render(request, 'delete_recipient.html', {'recipient': recipient})




def register_recipient(request):
    """
    Handles recipient registration.
    """
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipient registered successfully!')
            return redirect('blood_bank:recipient_list')
    else:
        form = RecipientForm()

    return render(request, 'register_recipient.html', {'form': form})

#inventoryyy

from django.shortcuts import render
from .models import BloodInventory

def blood_inventory(request):
    # Get all blood inventory data from the database
    blood_inventory = BloodInventory.objects.all()

    # Pass the data to the template
    return render(request, 'blood_inventory.html', {'blood_inventory': blood_inventory})


#trial donor reg

from django.shortcuts import render, redirect
from .forms import DonorRegForm

def donor_signup(request):
    if request.method == 'POST':
        form = DonorRegForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'signup_success.html')  # A success page template
    else:
        form = DonorRegForm()
    return render(request, 'donor2_signup.html', {'form': form})


#donor2 login view

# # views.py
# from django.shortcuts import render, redirect
# from .forms import DonorLoginForm
# from .models import DonorReg
# from django.contrib import messages

# # Donor Login
# def donor_login(request):
#     if request.user.is_authenticated:
#         return redirect('donor_dashboard')
#     if request.method == 'POST':
#         form = DonorLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             try:
#                 print("hi")
#                 donor = DonorReg.objects.get(username=username)
#                 if donor.password == password:  # Simple check (Use hashing in production)
#                     request.session['donor_id'] = donor.id
#                     print("hi2")
#                     # login(request, donor)
#                     return redirect('donor_dashboard')
#                 else:
#                     messages.error(request, "Invalid username or password.")
#             except DonorReg.DoesNotExist:
#                 messages.error(request, "Invalid username or password.")
#         return redirect('donor_login')
#     else:
#         form = DonorLoginForm()
#     return render(request, 'donor_login.html', {'form': form})

# # Donor Dashboard
# def donor_dashboard(request):
#     donor_id = request.session.get('donor_id')
#     if not donor_id:
#         return redirect('donor_login')

#     try:
#         donor = DonorReg.objects.get(id=donor_id)
#     except DonorReg.DoesNotExist:
#         return redirect('donor_login')

#     return render(request, 'donor_dashboard.html', {'donor': donor})

# # Donor Logout
# def donor_logout(request):
#     request.session.flush()
#     return redirect('donor_login')

from django.shortcuts import render, redirect
from .forms import DonorLoginForm
from .models import DonorReg
from django.contrib import messages

# Donor Login
def donor_login(request):
    if request.session.get('donor_id'):
        return redirect('donor_dashboard')

    if request.method == 'POST':
        form = DonorLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                donor = DonorReg.objects.get(username=username)
                if donor.password == password:  # Simple check (Use hashing in production)
                    request.session['donor_id'] = donor.id
                    return redirect('donor_dashboard')
                else:
                    messages.error(request, "Invalid username or password.")
            except DonorReg.DoesNotExist:
                messages.error(request, "Invalid username or password.")
        return redirect('donor_login')
    else:
        form = DonorLoginForm()
    return render(request, 'donor_login.html', {'form': form})

# Donor Dashboard
def donor_dashboard(request):
    donor_id = request.session.get('donor_id')
    if not donor_id:
        return redirect('donor_login')

    try:
        donor = DonorReg.objects.get(id=donor_id)
    except DonorReg.DoesNotExist:
        return redirect('donor_login')

    return render(request, 'donor_dashboard.html', {'donor': donor})

# Donor Logout
def donor_logout(request):
    request.session.flush()
    return redirect('donor_login')



#for the notification

