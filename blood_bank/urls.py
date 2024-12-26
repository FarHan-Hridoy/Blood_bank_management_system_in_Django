from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from blood_bank.views import donor_signup
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import donor_login, donor_dashboard, donor_logout, logout_view
# Define the app name for namespacing URLs

urlpatterns = [
    path('', views.home, name='home'),  # Default home page
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # Authentication paths
    path('accounts/login/', views.CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='blood_bank:home'), name='logout'),
    path('register/', views.register, name='register'),

    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Home and Profile paths
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    

    # Donor-related paths
    path('donors/', views.donor_list, name='donor_list'),
    path('donors/create/', views.create_donor, name='create_donor'),
    path('donors/<int:id>/edit/', views.edit_donor, name='edit_donor'),
    path('donors/<int:id>/delete/', views.delete_donor, name='delete_donor'),
    path('donor-signup/', views.donor_signup, name='donor2_signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', logout_view, name='logout'),
   
    # path('donor-login/', views.donor_login, name='donor_login'),  # Ensure this line is present
    # path('donor-dashboard/', views.donor_dashboard, name='donor_dashboard'),
    # path('donor-logout/', views.donor_logout, name='donor_logout'),
    path('donor-login/', donor_login, name='donor_login'),
    path('donor-dashboard/', donor_dashboard, name='donor_dashboard'),
    path('donor-logout/', donor_logout, name='donor_logout'),

    # Recipient-related paths
    path('recipients/', views.recipient_list, name='recipient_list'),
    path('recipients/create/', views.create_recipient, name='create_recipient'),
    path('recipients/<int:id>/edit/', views.edit_recipient, name='edit_recipient'),
    path('recipients/<int:id>/delete/', views.delete_recipient, name='delete_recipient'),
    # path('register-recipient/', views.create_recipient, name='register_recipient'),
    
    path('inventory/', views.blood_inventory, name='blood_inventory'),
    # Other paths...
    
    
]

# from django.urls import path
# from .views import donor_login, donor_dashboard, donor_logout

# urlpatterns = [
#     path('donor-login/', donor_login, name='donor_login'),
#     path('donor-dashboard/', donor_dashboard, name='donor_dashboard'),
#     path('donor-logout/', donor_logout, name='donor_logout'),
#     # other paths...
# ]