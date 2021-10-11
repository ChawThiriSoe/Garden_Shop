from django import forms
from .models import User
import re

class UserRegisterForm(forms.ModelForm):
    name = forms.CharField(label = 'Name',required = True, widget=forms.TextInput(attrs={'placeholder': 'Enter your Name'}))
    email = forms.EmailField(label = 'Email',required = True, widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
    password = forms.CharField(label = 'Password',required = True, widget = forms.PasswordInput(render_value = True,attrs={'placeholder': 'Enter a Password'}))
    
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password'
        ]

class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(label = 'Email',required = True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label = 'Password',required = True, widget = forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]

class UserEditForm(forms.ModelForm):
    name = forms.CharField(label = 'Name',required = True,widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label = 'Email',required = True, widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))

    class Meta:
        model = User
        fields = [
            'name',
            'email'
        ]

class UserFgPwdEmailAcceptForm(forms.ModelForm):
    email = forms.EmailField(label = 'Email',required = True, widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email'}))

    class Meta:
        model = User
        fields = [
            'email'
        ]

class UserResetPwdForm(forms.ModelForm):
    password = forms.CharField(label = 'Password',required = True, widget = forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    class Meta:
        model = User
        fields = [
            'password'
        ]

