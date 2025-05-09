from django.contrib.auth import get_user_model
User = get_user_model()

# authentication/forms.py
from django import forms

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','password']




class UserCreationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username','email','password','role']