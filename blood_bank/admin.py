from django.contrib import admin
from django.urls import path, include
from .models import BloodGroup, Donor, Recipient,Recipient2, Profile
from datetime import date
from .models import BloodInventory

@admin.register(BloodGroup)
class BloodGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'donation_date', 'is_active')  # Corrected to 'donation_date'
    search_fields = ('user__username', 'blood_group__name', 'location')
    list_filter = ('blood_group', 'is_active', 'donation_date')
    ordering = ['-donation_date']

    def age(self, obj):
        """Calculate and display donor's age."""
        return obj.age()

    age.short_description = 'Age'

    def is_eligible_for_donation(self, obj):
        """Check and display if the donor is eligible for donation."""
        return obj.is_eligible_for_donation()

    is_eligible_for_donation.short_description = 'Eligible for Donation'
    is_eligible_for_donation.boolean = True  # Display as a boolean in admin panel

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number', 'address')

# Custom admin configuration for Recipient
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'blood_group', 'contact', 'emergency_contact_name', 
        'emergency_contact_phone', 'needed_date', 'created_at', 'age'
    )
    search_fields = ('full_name', 'blood_group__name', 'contact', 'nid_number')
    ordering = ['-needed_date']
    list_filter = ('blood_group', 'created_at', 'needed_date')

    def age(self, obj):
        """Calculate and display recipient's age."""
        if obj.birth_date:
            today = date.today()
            age = today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
            return age
        return None

    age.short_description = 'Age'
    
    #recipiemt2
# @admin.register(Recipient2)
# class Recipient2Admin(admin.ModelAdmin):
#     list_display = ('user', 'username', 'full_name', 'blood_group', 'birth_date', 'address', 'contact', 'nid_number', 'by_date')
    #final recipient2
# from django.contrib import admin
# from .models import Recipient2

# @admin.register(Recipient2)
# class Recipient2Admin(admin.ModelAdmin):
#     list_display = ('username', 'full_name', 'blood_group','units', 'birth_date', 'address', 'contact', 'nid_number', 'by_date', 'status')
#     list_editable = ('status', 'units')  # Allows editing of status and units directly in the list view)
#     # list_editable = ('units',)
#     list_filter = ('status', 'blood_group')
#     actions = ['approve_requests', 'reject_requests']  # Add custom actions

#     def approve_requests(self, request, queryset):
#         queryset.update(status='Approved')
#         self.message_user(request, "Selected requests have been approved.")
#     approve_requests.short_description = "Approve selected requests"

#     def reject_requests(self, request, queryset):
#         queryset.update(status='Rejected')
#         self.message_user(request, "Selected requests have been rejected.")
#     reject_requests.short_description = "Reject selected requests"


#trial recipient2

from django.contrib import admin
from .models import Recipient2
from blood_bank.models import BloodInventory  # Assuming the app is named 'blood_bank'

@admin.register(Recipient2)
class Recipient2Admin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'blood_group', 'units', 'birth_date', 'address', 'contact', 'nid_number', 'by_date', 'status')
    list_editable = ('status', 'units')  # Allows editing of status and units directly in the list view
    list_filter = ('status', 'blood_group')
    actions = ['approve_requests', 'reject_requests']  # Add custom actions

    def approve_requests(self, request, queryset):
        approved_count = 0
        insufficient_units = []

        # Loop through the selected recipients in the queryset
        for recipient in queryset:
            if recipient.status != 'Approved':  # Only process if the recipient isn't already approved
                # Get the blood type as a string
                blood_type = str(recipient.blood_group)  # This assumes that __str__ method in BloodGroup returns the blood type (e.g., A+, O-)

                try:
                    # Look for matching blood type in the BloodInventory
                    inventory = BloodInventory.objects.get(blood_type=blood_type)
                except BloodInventory.DoesNotExist:
                    insufficient_units.append(f"{recipient.full_name} ({blood_type}) - Inventory not found.")
                    continue  # If inventory not found, skip this recipient

                # Check if there are enough units available in inventory
                if inventory.units >= recipient.units:
                    # If sufficient units, approve and update inventory
                    inventory.units -= recipient.units
                    inventory.save()

                    # Update recipient status to approved
                    recipient.status = 'Approved'
                    recipient.save()

                    approved_count += 1
                else:
                    # If not enough units, add to the insufficient units list
                    insufficient_units.append(f"{recipient.full_name} ({blood_type}) - Not enough units. Requested: {recipient.units}, Available: {inventory.units}")

        # Feedback for the admin in the Django Admin interface
        if approved_count > 0:
            self.message_user(request, f"{approved_count} recipient(s) approved, and inventory updated.")
        if insufficient_units:
            self.message_user(
                request,
                "Some requests could not be approved due to insufficient units:\n" + "\n".join(insufficient_units),
                level='error'
            )

    approve_requests.short_description = "Approve selected requests and update inventory"

    def reject_requests(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, "Selected requests have been rejected.")
    reject_requests.short_description = "Reject selected requests"




#inventory


# class BloodInventoryAdmin(admin.ModelAdmin):
#  list_display = ('blood_type', 'units', 'capacity')
# search_fields = ('blood_type',)
# list_editable = ('units', 'capacity')  # Allows editing of units and capacity directly in the list view
# admin.site.register(BloodInventory, BloodInventoryAdmin)

from django.contrib import admin
from .models import BloodInventory

class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_type', 'units', 'capacity')  # Fields to display
    list_editable = ('units', 'capacity')  # Fields to allow inline editing
    list_display_links = ('blood_type',)  # Only 'blood_type' is clickable

admin.site.register(BloodInventory, BloodInventoryAdmin)


#New donor reg

# from django.contrib import admin
# from .models import DonorReg

# @admin.register(DonorReg)
# class DonorRegAdmin(admin.ModelAdmin):
#     list_display = ('username', 'full_name', 'blood_group','last_donation_date', 'phone', 'email', 'emergency_donor', 'status')
#     search_fields = ('username', 'full_name', 'blood_group', 'email')
#     list_filter = ('blood_group', 'emergency_donor')
    
#     #trial new
#     list_editable = ('status',)
#     # list_filter = ('status', 'blood_group')
#     actions = ['approve_requests', 'reject_requests']  # Add custom actions

#     def approve_requests(self, request, queryset):
#         queryset.update(status='Approved')
#         self.message_user(request, "Selected requests have been approved.")
#     approve_requests.short_description = "Approve selected requests"

#     def reject_requests(self, request, queryset):
#         queryset.update(status='Rejected')
#         self.message_user(request, "Selected requests have been rejected.")
#     reject_requests.short_description = "Reject selected requests"


from django.contrib import admin
from .models import DonorReg
from blood_bank.models import BloodInventory  # Replace 'blood_bank' with the actual app name

@admin.register(DonorReg)
class DonorRegAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'blood_group', 'last_donation_date','dob', 'phone', 'email', 'emergency_donor', 'status', 'gender')
    search_fields = ('username', 'full_name', 'blood_group', 'email')
    list_filter = ('blood_group', 'emergency_donor')
    
    list_editable = ('status',)
    actions = ['approve_requests', 'reject_requests']  # Add custom actions

    def approve_requests(self, request, queryset):
        approved_count = 0  # Counter for approved donors

        for donor in queryset:
            if donor.status != 'Approved':  # Only process if not already approved
                donor.status = 'Approved'  # Update donor status
                donor.save()
                approved_count += 1

                # Update or create a BloodInventory record
                inventory, created = BloodInventory.objects.get_or_create(
                    blood_type=donor.blood_group,
                    defaults={'units': 0, 'capacity': 100}  # Default capacity
                )

                # Increment the blood units
                inventory.units += 1
                inventory.save()

        # Display a success message in the admin panel
        self.message_user(
            request,
            f"{approved_count} donor(s) approved, and inventory updated successfully."
        )

    approve_requests.short_description = "Approve selected requests and update inventory"

    def reject_requests(self, request, queryset):
        rejected_count = queryset.update(status='Rejected')  # Bulk update to 'Rejected'
        self.message_user(
            request,
            f"{rejected_count} donor(s) rejected."
        )
    reject_requests.short_description = "Reject selected requests"
