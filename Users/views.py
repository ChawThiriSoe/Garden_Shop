from django.shortcuts import redirect, render
from .models import User
from .forms import UserRegisterForm,UserLoginForm

# Create your views here.

def User_Register_View(request):
    if request.method == 'POST':
        userForm = UserRegisterForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            userForm = UserRegisterForm()
            return redirect('users:user-login')
        context = {
        'userForm' : userForm
        }
        return render(request, "register.html", context)
    else:
        userForm = UserRegisterForm()
        context = {
        'userForm' : userForm
        }
        return render(request, "register.html", context)

def User_Login_View(request):
    if request.method == 'POST':
        userForm = UserLoginForm(request.POST)
        if userForm.is_valid():
            username = userForm.cleaned_data['name']
            password = userForm.cleaned_data['password']
            
            if User.objects.filter(name=username, password=password).exists():
                return render(request, "index.html")
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