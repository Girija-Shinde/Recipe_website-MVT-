from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import UserProfile
import re
import requests
from django.conf import settings


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profile_picture')
        recaptcha_response = request.POST.get('g-recaptcha-response') 

        # Validate reCAPTCHA response
        recaptcha_secret_key = settings.RECAPTCHA_PRIVATE_KEY  
        recaptcha_verification_url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {'secret': recaptcha_secret_key, 'response': recaptcha_response}
        recaptcha_response = requests.post(recaptcha_verification_url, data=data)
        recaptcha_result = recaptcha_response.json()
        # print(recaptcha_result)

        if not recaptcha_result.get('success'):
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})

        # Validate form fields
        if not all([username, email, password, confirm_password]):
            messages.error(request, "All fields are mandatory")
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})

        if password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email ID already exists!")
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})

        try:
            validate_email(email)  
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})
        
        # Password strength validation
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})

        if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', username):
            messages.error(request, 'Username must be alphanumeric and should not start with a number.')
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})
        
        # Check password complexity
        if not any(char.isdigit() for char in password) or not any(char.islower() for char in password) or \
           not any(char.isupper() for char in password) or not any(char in '!@#$%^&*' for char in password):
            messages.error(request, 'Password is too weak. It must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})

        # Create the user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})
        
        # Handle profile picture
        if profile_picture:
            if not profile_picture.name.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                messages.error(request, 'Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.')
                return render(request, 'custom_auth/register.html', {'title': 'Register', 'RECAPTCHA_PUBLIC_KEY':settings.RECAPTCHA_PUBLIC_KEY})

        UserProfile.objects.create(user=user, profile_pic=profile_picture if profile_picture else None)

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'custom_auth/register.html', {'title': 'Register','RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})

# def register_page(request):
#     if request.user.is_authenticated:
#         return redirect('home')
    
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         profile_picture = request.FILES.get('profile_picture')

#         # Validate form fields
#         if not all([username, email, password, confirm_password]):
#             messages.error(request, "All fields are mandatory")
#             return render(request, 'custom_auth/register.html')

#         if password != confirm_password:
#             messages.error(request, "Passwords don't match!")
#             return render(request, 'custom_auth/register.html')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists!")
#             return render(request, 'custom_auth/register.html')

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email ID already exists!")
#             return render(request, 'custom_auth/register.html')

#         try:
#             validate_email(email)  
#         except ValidationError:
#             messages.error(request, "Invalid email address.")
#             return render(request, 'custom_auth/register.html')
        
#         # Password strength validation
#         try:
#             validate_password(password)
#         except ValidationError as e:
#             messages.error(request, str(e))
#             return render(request, 'custom_auth/register.html')

#         if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', username):
#             messages.error(request, 'Username must be alphanumeric and should not start with a number.')
#             return render(request, 'custom_auth/register.html')
        
#         # Check password complexity
#         if not any(char.isdigit() for char in password) or not any(char.islower() for char in password) or \
#            not any(char.isupper() for char in password) or not any(char in '!@#$%^&*' for char in password):
#             messages.error(request, 'Password is too weak. It must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
#             return render(request, 'custom_auth/register.html')

#         # Create the user
#         try:
#             user = User.objects.create_user(username=username, email=email, password=password)
#         except ValidationError as e:
#             messages.error(request, str(e))
#             return render(request, 'custom_auth/register.html')
        
#         # Handle profile picture
#         if profile_picture:
#             if not profile_picture.name.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
#                 messages.error(request, 'Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.')
#                 return render(request, 'custom_auth/register.html')

#         UserProfile.objects.create(user=user, profile_pic=profile_picture if profile_picture else None)

#         messages.success(request, 'Registration successful! Please log in.')
#         return redirect('login')

#     return render(request, 'custom_auth/register.html', {'title': 'Register'})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,'Login successful!') 
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "custom_auth/login.html", {'title': 'Login'}) 
    
    # Render login form for GET requests
    return render(request, 'custom_auth/login.html', {'title': 'Login'})


def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required
def my_profile(request):
    user_profile = get_object_or_404(UserProfile, user = request.user)
    return render(request, 'custom_auth/my_profile.html', {'user_profile': user_profile, 'title': 'My Profile'})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile

        new_username = request.POST.get('username')
        if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', new_username):
            messages.error(request, 'Username must be alphanumeric and should not start with a number.')
            return redirect('edit_profile')
        elif new_username != request.user.username and User.objects.filter(username = new_username):
            messages.error(request, 'Username already exists!')
            return redirect('edit_profile')
        else:
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Username updated successfully!')

        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            if not profile_pic.name.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                messages.error(request, 'Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.')
                return render(request, 'custom_auth/edit_profile.html', {'user_profile': user_profile, 'title': 'Edit Profile'})
            user_profile.profile_pic = profile_pic
            user_profile.save()
        
        bio = request.POST.get('bio')
        if bio:
            if len(bio) > 150:  # Example max length
                messages.error(request, 'Bio cannot exceed 150 characters.')
                return render(request, 'custom_auth/edit_profile.html', {'user_profile': user_profile, 'title': 'Edit Profile'})
            user_profile.bio = bio
            user_profile.save()
        return redirect('my_profile')
    
    user_profile = request.user.userprofile
    return render(request, 'custom_auth/edit_profile.html',{'user_profile': user_profile, 'title': 'Edit Profile'})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect')
            return redirect('change_password')
        
        if old_password == new_password:
            messages.error(request, 'Old and new passwords cannot be the same')
            return redirect('change_password')
        
        if new_password != confirm_password:
            messages.error(request, "New password doesn't match the confirm password")
            return redirect('change_password')
        
        if not any(char.isdigit() for char in new_password) or not any(char.islower() for char in new_password) or \
           not any(char.isupper() for char in new_password) or not any(char in '!@#$%^&*' for char in new_password):
            messages.error(request, 'Password is too weak. It must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
            return redirect('change_password')

        try:
            validate_password(new_password, user=request.user)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('change_password')
        
        request.user.set_password(new_password)
        request.user.save()

        # Update the session with the new password to avoid log out
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password updated successfully!')
        return redirect('home')
    
    return render(request, 'custom_auth/change_password.html', {'title': 'Change Password'})
