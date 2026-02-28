from django import forms
from Registration.models import Registration



class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']