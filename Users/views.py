from django.shortcuts import redirect, render
from .models import User,Product,Order
from .forms import (UserRegisterForm,
                    UserLoginForm,
                    UserEditForm,
                    UserFgPwdEmailAcceptForm,
                    UserResetPwdForm,
                    )
import re,hashlib

# Create your views here.

def Index_View(request):
    return render(request,"index.html")

def pwd_encode(pwd):
    # to imporve security by using md5 algorithm.
    md5_pwd =hashlib.md5(pwd.encode()).hexdigest()
    secure_pwd = hashlib.sha256(md5_pwd.encode()).hexdigest()
    return secure_pwd

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
                    name = userForm.cleaned_data['name']
                    email = userForm.cleaned_data['email']
                    password = pwd_encode(userpwd)
                    user_info = User(name=name, email=email, password=password)
                    user_info.save()
                    return redirect('users:user-login')
                    break
            if condition_pwd == -1:
                context = {
                    'userForm':userForm,
                    'error':err_msg
                }
                return render(request,"register.html",context)
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
            email = userForm.cleaned_data['email']
            password = pwd_encode(userForm.cleaned_data['password'])
            
            if User.objects.filter(email=email, password=password).exists():
                user_data=User.objects.get(email=email,password=password)
                request.session['username'] = user_data.name
                request.session['logged'] =True
                request.session['image'] = str(user_data.image)
                request.session['id'] = user_data.id
                request.session['email'] = user_data.email
                request.session['password'] = user_data.password
                return redirect('users:index')
            else:
                userForm = UserLoginForm()
                error = "Invalid Input. Please try again"
                context = {
                    'userForm': userForm,
                    'error':error
                }
                return render(request, "login.html", context)
        else:
            userForm = UserLoginForm()
            error = "Invalid Input. Please try again"
            context = {
                'userForm': userForm,
                'error':error
            }
            return render(request, "login.html", context)
    else:
        userForm = UserLoginForm()
        context = {'userForm': userForm}
        return render(request, 'login.html', context)

def User_Logout(request):
    print(request.session['image'])
    del request.session['username']
    request.session['logged'] = False
    del request.session['image']
    del request.session['id']
    del request.session['email']
    del request.session['password']
    
    return redirect('users:index')

def User_Profile(request,id):
    if request.method == 'POST':
        userdata = User.objects.get(id=id)
        userForm = UserEditForm(request.POST,instance = userdata)
        if userForm.is_valid():
            userForm.save()
            name = userForm.cleaned_data["name"]
            email = userForm.cleaned_data["email"]
            request.session['username'] = name
            request.session['email'] = email
            
            userForm = UserEditForm(initial={'name': userdata.name, 'email':userdata.email } ) 
            context ={

                'form':userForm
            }
    
            return render(request,'user_profile.html',context)
    else:
        userdata = User.objects.get(id=id)
        userForm = UserEditForm(initial={'name': userdata.name, 'email':userdata.email } ) 
        context ={
            'form':userForm
        }
    
        return render(request,'user_profile.html',context)
    
def User_FgPwd_Email_Accept_View(request):
    if request.method == 'POST':
        userForm = UserFgPwdEmailAcceptForm(request.POST)
        if userForm.is_valid():
            email = userForm.cleaned_data['email']
            
            if User.objects.filter(email=email).exists():
                user_data=User.objects.get(email=email)
                request.session['email'] = user_data.email
                return redirect('users:user-reset-pwd') 
    else:
        userForm = UserFgPwdEmailAcceptForm()
        context = {
            'form': userForm
        }
        return render(request,'fgpwdemailaccept.html',context)

def User_Reset_Pwd_View(request):
    if request.method == 'POST':
        userForm = UserResetPwdForm(request.POST)
        if userForm.is_valid():
            newpwd = userForm.cleaned_data['password']
            
            if User.objects.filter(email=request.session['email']).exists():
                user_data=User.objects.get(email=request.session['email'])
                password = user_data.password
                if password == pwd_encode(newpwd):
                    error = "New password cannot be the same with old password!!"
                    context = {
                        'form': userForm,
                        'error': error
                    }
                    return render(request,'resetpwd.html',context)
                else:
                    condition_pwd = 0
                    err_msg = ''
                    while True:
                        if (len(newpwd)<8):
                            condition_pwd = -1
                            err_msg = "Password lenght must contain at least 8 characters."
                            break
                        elif not re.search('[a-z]', newpwd):
                            condition_pwd = -1
                            err_msg = "Password must contain at least one small letter characters."
                            break
                        elif not re.search('[A-Z]', newpwd):
                            condition_pwd = -1
                            err_msg = "Password must contain at least one capital letter characters."
                            break
                        elif not re.search('[0-9]', newpwd):
                            condition_pwd = -1
                            err_msg = "Password must contain at least one number."
                            break
                        elif not re.search('[!@#$%&_]', newpwd):
                            condition_pwd = -1
                            err_msg = "Password must contain at least one special characters."
                            break
                        elif re.search('\s', newpwd):
                            condition_pwd = -1
                            err_msg = "Password must not contain whitespace character."
                            break
                        else: 
                            condition_pwd = 0
                            hashpwd = pwd_encode(newpwd)
                            User.objects.filter(email=request.session['email']).update(password=hashpwd)
                            del request.session['email']
                            return redirect('users:user-login')
                            break
                    if condition_pwd == -1:
                        context = {
                            'userForm':userForm,
                            'error':err_msg
                        }
                        return render(request,'resetpwd.html',context)
            else:
                context = {
                    'userForm':userForm
                }
                return render(request,'resetpwd.html',context)

    else:
        userForm = UserResetPwdForm()
        context = {
            'form': userForm
        }
        return render(request,'resetpwd.html',context)

def Fruits_View(request):
    if 'add_to_cate' in request.POST:
        userdata = User.objects.get(name=request.session['username'])
        productdata = Product.objects.get(name=request.POST.get("fruit_name"))
        qty = request.POST.get("quantity")
        cost = float(productdata.price) * float(qty)

        new_entry = Order(user=userdata, product=productdata, quantity=qty, cost=cost, status=False)
        new_entry.save()
        
    elif 'add_to_wishlist' in request.POST:

        return render(request,'user_profile.html')
    fruit_obj = Product.objects.filter(categories='Fruit')
    context = {
        'fruit_obj' : fruit_obj
    }
    return render(request,'fruits.html',context)

def Vegetables_View(request):
    if 'add_to_cate' in request.POST:
        userdata = User.objects.get(name=request.session['username'])
        productdata = Product.objects.get(name=request.POST.get("vegetable_name"))
        qty = request.POST.get("quantity")
        cost = float(productdata.price) * float(qty)

        new_entry = Order(user=userdata, product=productdata, quantity=qty, cost=cost, status=False)
        new_entry.save()
        
    elif 'add_to_wishlist' in request.POST:

        return render(request,'user_profile.html')
    vegetable_obj = Product.objects.filter(categories='Vegetable')
    context = {
        'vegetable_obj' : vegetable_obj
    }
    return render(request,'Vegetables.html',context)