from django import forms
import re
from .models import User

class UserRegisterForm(forms.ModelForm):
    name = forms.CharField(label="Name", required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)
    
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password'
        ]

    def clean_password(self, *args, **kwargs):
        userpwd = self.cleaned_data.get("password")
        condition_pwd = 0
        err_msg = ''
        while True:
            if (len(userpwd)<8):
                condition_pwd = -1
                err_msg = "Password's length must contain at least 8 characters."
                break
            elif not re.search('[a-z]', userpwd):
                condition_pwd = -1
                err_msg = "Password must contain at least one small letter characters."
                break
            elif not re.search('[A-Z]', userpwd):
                condition_pwd = -1
                err_msg = "Password must contain at least one capital letter characters."
                break
            elif not re.search('[0-9]', userpwd):
                condition_pwd = -1
                err_msg = "Password must contain at least one number."
                break
            elif not re.search('[!@#$%&_]', userpwd):
                condition_pwd = -1
                err_msg = "Password must contain at least one special characters."
                break
            elif re.search('\s', userpwd):
                condition_pwd = -1
                err_msg = "Password must not contain whitespace character."
                break
            else: 
                condition_pwd = 0
                return userpwd
        if condition_pwd == -1:
            raise forms.ValidationError(err_msg)

class UserLoginForm(forms.ModelForm):
    name = forms.CharField(label="Name", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)

    class Meta:
        model = User
        fields = [
            'name',
            'password'
        ]
    
