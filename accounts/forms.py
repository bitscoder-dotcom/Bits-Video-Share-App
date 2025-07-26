from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CreatorProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

class CreatorApplicationForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = ['channel_name', 'channel_description']
