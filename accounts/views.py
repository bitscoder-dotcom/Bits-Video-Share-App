from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, CreatorApplicationForm
from .models import CreatorProfile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Authenticate explicitly using username and password
            raw_password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(
                request, username=user.username, password=raw_password
            )

            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, 'Registration successful!')
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed. Please login manually.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    context = {}
    if request.user.user_type == 2:  # Creator
        try:
            context['creator_profile'] = request.user.creator_profile
        except CreatorProfile.DoesNotExist:
            pass
    return render(request, 'accounts/dashboard.html', context)

@login_required
def become_creator(request):
    if request.user.user_type == 2:
        messages.info(request, 'You are already a creator!')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CreatorApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            creator_profile = form.save(commit=False)
            creator_profile.user = request.user
            creator_profile.save()
            
            # Update user type to creator
            user = request.user
            user.user_type = 2
            user.save()
            
            messages.success(request, 'Your creator application has been submitted!')
            return redirect('dashboard')
    else:
        form = CreatorApplicationForm()
    
    return render(request, 'accounts/creator_apply.html', {'form': form})
