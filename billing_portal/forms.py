from django import forms
from django.contrib.auth.models import User
from .models import Company

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'})
        }

class RegisterCompanyForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}))
