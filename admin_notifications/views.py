# views.py
from django.http import JsonResponse
from admin_notifications.models import Notification

def some_view(request):
    # Create notification for the logged-in user
    Notification.objects.create(
        recipient=request.user,
        title="Welcome!",
        message="Welcome to our platform.",
        notification_type="success"
    )
    # ... rest of your view code
    from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
@require_POST
def mark_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)
    
    # views.py
from admin_notifications.models import Notification

from django import forms

class ContactForm(forms.Form):
    # Define your form fields here
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

def contact_form_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form
            form.save()
            
            # Create notification for admin
            admin_user = User.objects.filter(is_superuser=True).first()
            Notification.objects.create(
                recipient=admin_user,
                title="New Contact Form Submission",
                message="Someone has submitted the contact form.",
                notification_type="info"
            )
        
        # views.py
from django.shortcuts import render
from admin_notifications.models import Notification

def my_notifications(request):
    notifications = Notification.objects.filter(
        recipient=request.user,
        read=False
    )
    return render(request, 'my_notifications.html', {
        'notifications': notifications
    })