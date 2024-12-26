from django.contrib import admin
from .models import Recipient2

@admin.register(Recipient2)
class Recipient2Admin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'blood_group', 'birth_date', 'address', 'contact', 'nid_number', 'by_date', 'status')
    list_editable = ('status',)
    list_filter = ('status', 'blood_group')
    actions = ['approve_requests', 'reject_requests']  # Add custom actions

    def approve_requests(self, request, queryset):
        queryset.update(status='Approved')
        self.message_user(request, "Selected requests have been approved.")
    approve_requests.short_description = "Approve selected requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, "Selected requests have been rejected.")
    reject_requests.short_description = "Reject selected requests"