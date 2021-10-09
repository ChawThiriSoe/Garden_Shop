from django.shortcuts import redirect, render
from .models import User
from .forms import UserRegisterForm,UserLoginForm
import re

# Create your views here.

def Index_View(request):
    return render(request,"index.html")

def User_Register_View(request):
    if request.method == 'POST':
        userForm = UserRegisterForm(request.POST)
        if userForm.is_valid():
            userpwd = userForm.cleaned_data["password"]
            condition_pwd = 0
            err_msg = ''
            while True:
                if (len(userpwd)<8):
                    condition_pwd = -1
                    err_msg = "Password lenght must contain at least 8 characters."
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
                    break
            if condition_pwd == -1:
                context = {
                    'userForm':userForm,
                    'error':err_msg
                }
                return render(request,"register.html",context)
            else:
                userForm.save()
                return redirect('users:user-login')
        else:
            context = {
            'userForm':userForm
        }
            return render(request,"register.html",context)
    else:
        userForm = UserRegisterForm()
        context = {
            'userForm':userForm
        }
        return render(request,"register.html",context)

def User_Login_View(request):
    if request.method == 'POST':
        userForm = UserLoginForm(request.POST)
        if userForm.is_valid():
            username = userForm.cleaned_data['name']
            password = userForm.cleaned_data['password']
            
            if User.objects.filter(name=username, password=password).exists():
                user_data=User.objects.get(name=username,password=password)
                request.session['username'] = user_data.name
                return redirect('users:index')
            else:
                userForm = UserLoginForm()
                context = {
                    'userForm': userForm
                }
                return render(request, "login.html", context)
    else:
        userForm = UserLoginForm()
        context = {'userForm': userForm}
        return render(request, 'login.html', context)