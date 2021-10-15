from django.shortcuts import redirect, render
from .models import User,Product,Order
from .forms import (UserRegisterForm,
                    UserLoginForm,
                    UserEditForm,
                    UserEditPasswordForm,
                    UserFgPwdEmailAcceptForm,
                    UserResetPwdForm,

                    )
import re,hashlib

# Create your views here.

def Shopping_cart(request,user_id):
    product_img_qty_data = {}
    total_cost = 0.0
    if Order.objects.filter(user=user_id):
        data = Order.objects.filter(user=user_id,status=False)
        for one_obj in data:
            product_img_qty_data[str(one_obj.product.image)] = [one_obj.quantity,one_obj.id]
            total_cost += float(one_obj.cost)
    request.session['product_img_qty_data']=product_img_qty_data
    request.session['total_cost']=total_cost

def pwd_encode(pwd):
    # to imporve security by using md5 algorithm.
    md5_pwd =hashlib.md5(pwd.encode()).hexdigest()
    secure_pwd = hashlib.sha256(md5_pwd.encode()).hexdigest()
    return secure_pwd

def pwd_check(userpwd):
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
            errmsg = "Password must contain at least one number."
            break
        elif not re.search('[!@#$%&]', userpwd):
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

    return condition_pwd,err_msg

def Index_View(request):
    return render(request,"index.html")

def User_Register_View(request):
    if request.method == 'POST':
        userForm = UserRegisterForm(request.POST)
        if userForm.is_valid():
            userpwd = userForm.cleaned_data["password"]
            name = userForm.cleaned_data['name']
            email = userForm.cleaned_data['email']
            exist_name = User.objects.filter(name=name)
            exist_email = User.objects.filter(email=email)
            if exist_name.exists():
                error='User Already Existed'
                context = {
                    'userForm':userForm,
                    'error':error
                }
                return render(request,"register.html",context)
            elif exist_email.exists():
                error='Email Already Existed'
                context = {
                    'userForm':userForm,
                    'error':error
                }
                return render(request,"register.html",context)
            else:
                condition_pwd,err_msg = pwd_check(userpwd)

                if condition_pwd == 0:

                    password = pwd_encode(userpwd)
                    user_info = User(name=name, email=email, password=password)
                    user_info.save()
                    return redirect('users:user-login')

                elif condition_pwd == -1:
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

                Shopping_cart(request,request.session['id'])

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
    if 'product_img_qty_data' in request.session:
        del request.session['product_img_qty_data']
        del request.session['total_cost']
    else:
        return redirect('users:index')
    return redirect('users:index')

def User_Profile(request):
    if request.method == 'POST':
        userdata = User.objects.get(id=request.session['id'])
        userForm = UserEditForm(request.POST,instance = userdata)
        if userForm.is_valid():
            username = User.objects.exclude(name = userdata.name,email=userdata.email)
            for user in username:
                print(user)
                if userForm.cleaned_data["name"] == user.name:
                    error="Name unavailable"
                    userForm = UserEditForm(initial={'name': request.session['username'], 'email':request.session['email'] } ) 
                    context ={

                        'form':userForm,
                        'error':error
                    }
    
                    return render(request,'user_profile.html',context)
                elif userForm.cleaned_data["email"] == user.email:
                    error="Email unavailable"
                    print("email error mtr fkr")
                    print(userForm.cleaned_data["email"])
                    print(user.email)
                    userForm = UserEditForm(initial={'name': request.session['username'], 'email':request.session['email'] } ) 
                    context ={

                        'form':userForm,
                        'error':error
                    }
    
                    return render(request,'user_profile.html',context)
                else:

                    userForm.save()
                    name = userForm.cleaned_data["name"]
                    email = userForm.cleaned_data["email"]
                    request.session['username'] = name
                    request.session['email'] = email
            
                    userForm = UserEditForm(initial={'name': userdata.name, 'email':userdata.email } ) 
                    noerror ="Save Changes"
                    context ={

                        'form':userForm,
                        'noerror':noerror
                    }
    
                    return render(request,'user_profile.html',context)
    else:
        userdata = User.objects.get(id=request.session['id'])
        userForm = UserEditForm(initial={'name': userdata.name, 'email':userdata.email } ) 
        context ={

            'form':userForm
        }
    
        return render(request,'user_profile.html',context)

def Get_Old_Password(request):
    if request.method == 'POST':
        current_pwd = request.POST.get("currentpwd")
        if User.objects.filter(email=request.session['email']).exists():
                user_data=User.objects.get(email=request.session['email'])
                password = user_data.password
                
                if pwd_encode(current_pwd) == password:
                    return redirect('users:user-password')
                else:
                    error = "Password not matched"
                    context = {
                        'error':error
                    }
                    return render(request,'get_old_password.html',context)
    else:
        return render(request,'get_old_password.html')

def User_Password(request):
    if request.method == 'POST':
        
        
        form = UserEditPasswordForm(request.POST)
        if form.is_valid():
            userpwd = form.cleaned_data["password"]
            if User.objects.filter(email=request.session['email']).exists():
                user_data=User.objects.get(email=request.session['email'])
                password = user_data.password
                if password == pwd_encode(userpwd):
                    error = "New password cannot be the same with old password!!"
                    context = {
                        'form': form,
                        'error': error
                    }
                    return render(request,'password_edit.html',context)
                else:
                    condition_pwd,err_msg = pwd_check(userpwd)

                    if condition_pwd == 0:
                        password = form.cleaned_data['password']
                        secure_password = pwd_encode(userpwd)
                    
                        User.objects.filter(email=request.session['email']).update(password=secure_password)
                    
                       
                        context = {
                            'form':form,
                        }
                        return redirect('users:user-profile')

                    elif condition_pwd == -1:
                        print(err_msg)
                        context = {
                            'form':form,
                            'error':err_msg
                    
                        }
                        return render(request,"password_edit.html",context)

        else:
            form = UserEditPasswordForm()
            
            context = {
                'form':form,
                
                
            }
            return render(request,'password_edit.html',context)

    else:
        form = UserEditPasswordForm()
        
        context = {
            'form':form,
            
        }
        return render(request,'password_edit.html',context)
    
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
                    condition_pwd,err_msg = pwd_check(newpwd)

                    if condition_pwd == 0:
                        hashpwd = pwd_encode(newpwd)
                        User.objects.filter(email=request.session['email']).update(password=hashpwd)
                        del request.session['email']
                        return redirect('users:user-login')

                    elif condition_pwd == -1:
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
    if 'add_to_cart' in request.POST:
        userdata = User.objects.get(name=request.session['username'])
        productdata = Product.objects.get(name=request.POST.get("fruit_name"))
        qty = request.POST.get("quantity")
        print(request.POST.get("fruit_name"))
        cost = float(productdata.price) * float(qty)

        obj = Order.objects.filter(user=userdata,product=productdata)
        if obj.exists():
            obj.delete()

        new_entry = Order(user=userdata, product=productdata, quantity=qty, cost=cost, status=False)
        new_entry.save()
        
        Shopping_cart(request,request.session['id'])
        
    elif 'add_to_wishlist' in request.POST:

        return render(request,'user_profile.html')
    fruit_obj = Product.objects.filter(categories='Fruit')
    context = {
        'fruit_obj' : fruit_obj
    }
    return render(request,'fruits.html',context)

def Vegetables_View(request):
    if 'add_to_cart' in request.POST:
        userdata = User.objects.get(name=request.session['username'])
        productdata = Product.objects.get(name=request.POST.get("vegetable_name"))
        qty = request.POST.get("quantity")
        cost = float(productdata.price) * float(qty)

        obj = Order.objects.filter(user=userdata,product=productdata)
        if obj.exists():
            obj.delete()

        new_entry = Order(user=userdata, product=productdata, quantity=qty, cost=cost, status=False)
        new_entry.save()

        Shopping_cart(request,request.session['id'])
        
    elif 'add_to_wishlist' in request.POST:

        return render(request,'user_profile.html')
    vegetable_obj = Product.objects.filter(categories='Vegetable')
    context = {
        'vegetable_obj' : vegetable_obj
    }
    return render(request,'Vegetables.html',context)

def Cart_Item_Delete(request):
    if request.method == 'POST':
        order_id = request.POST.get("order_id")
        obj = Order.objects.get(id=order_id)
        obj.delete()
        Shopping_cart(request,request.session['id'])
        return redirect(request.META.get('HTTP_REFERER'))