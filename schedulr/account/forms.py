from django import forms
from django.contrib.auth import password_validation


class InitialSetupForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, strip=False)

    def clean_password(self):
        password = self.cleaned_data["password"]
        password_validation.validate_password(password)
        return password


class SessionSetupForm(forms.Form):
    name = forms.CharField(required=True)
