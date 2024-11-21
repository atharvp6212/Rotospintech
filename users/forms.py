from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'is_worker', 'is_admin')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'is_worker', 'is_admin')
        
class WorkerCreationForm(UserCreationForm):
    can_add_stock = forms.BooleanField(required=False)
    can_add_order = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'can_add_stock', 'can_add_order')
