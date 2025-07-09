from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .forms import CustomUserRegistrationForm, CustomLoginForm, UserProfileUpdateForm, UserUpdateForm
from .models import UserProfile


class RegisterView(View):
    """User registration view with success message"""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:home')
        
        form = CustomUserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('products:home')
        
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Add success message
            messages.success(
                request, 
                f'🎉 Welcome {user.first_name}! Your account has been created successfully. '
                f'You can now sign in with your credentials.'
            )
            
            # Optionally auto-login the user
            # login(request, user)
            # return redirect('products:home')
            
            # Redirect to login page
            return redirect('accounts:login')
        
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    """User login view with remember me functionality"""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:home')
        
        form = CustomLoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('products:home')
        
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            
            # Try to authenticate by username first
            user = authenticate(request, username=username_or_email, password=password)
            
            # If that fails, try to find user by email
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                
                # Handle remember me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                # Success message
                messages.success(request, f'Welcome back, {user.first_name or user.username}! 🎉')
                
                # Redirect to next page or home
                next_page = request.GET.get('next', 'products:home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username/email or password. Please try again.')
        
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    """User logout view"""
    
    def get(self, request):
        if request.user.is_authenticated:
            user_name = request.user.first_name or request.user.username
            logout(request)
            messages.success(request, f'You have been successfully logged out. See you soon, {user_name}! 👋')
        
        return redirect('products:home')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """User profile view and update"""
    
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_form = UserProfileUpdateForm(instance=profile)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'accounts/profile.html', context)
    
    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_form = UserProfileUpdateForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully! ✅')
            return redirect('accounts:profile')
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'accounts/profile.html', context)
