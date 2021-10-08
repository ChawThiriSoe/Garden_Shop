from django import forms
from .models import User

class UserRegisterForm(forms.ModelForm):
    name = forms.CharField(label = 'Name',required = True, widget=forms.TextInput(attrs={'placeholder': 'Enter your Name'}))
    email = forms.EmailField(label = 'Email',required = True, widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
    password = forms.CharField(label = 'Password',required = True, widget = forms.PasswordInput(attrs={'placeholder': 'Enter a Password'}))

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password'
        ]

class UserLoginForm(forms.ModelForm):
    name = forms.CharField(label = 'Name',required = True,widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label = 'Password',required = True, widget = forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = [
            'name',
            'password'
        ]