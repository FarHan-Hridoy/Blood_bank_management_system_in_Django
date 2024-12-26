from django.urls import path
from . import views

app_name = 'admin_notifications'

urlpatterns = [
    path('mark-as-read/<int:notification_id>/', 
         views.mark_as_read, 
         name='mark_as_read'),
]