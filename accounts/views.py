from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

def check_role_rest(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied
    
def check_role_cust(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied    
    


# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        user=request.user
        redirecturl=detectUser(user)
        return redirect(redirecturl)
    elif request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role=User.CUSTOMER
            user.set_password(password)
            user.save()
            messages.success(request, "your registsration has been successfully done")
            return redirect('registerUser')
        else:
            print(form.errors)
    else:    
        form = UserForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/userRegister.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        user=request.user
        redirecturl=detectUser(user)
        return redirect(redirecturl)
    elif request.method=='POST':
        form=UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role=User.RESTUARANT
            user.set_password(password)
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user = user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,"Your Restuarant is successfully registered")
            return redirect('registerVendor')
        else:
            print(form.errors)
            print(v_form.errors)
    else:    
        form=UserForm()
        v_form = VendorForm()
    context = {
        'form':form,
        'v_form':v_form,
    }
    return render(request, 'accounts/registerVendor.html',context)


def login(request):
    if request.user.is_authenticated:
        user=request.user
        redirecturl=detectUser(user)
        return redirect(redirecturl)
    elif request.method=='POST':
        email=request.POST.get('email')        
        password=request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        print(user,email,password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, 'you are logged in now')
            user=request.user
            redirecturl=detectUser(user)
            return redirect(redirecturl)
        else:
            messages.error(request,"credantials are wrong")
            return redirect('login')
                
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"youre now logout")
    return redirect('login')
@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirecturl=detectUser(user)
    return redirect(redirecturl)

@login_required(login_url='login')
@user_passes_test(check_role_cust)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_rest)
def restDashboard(request):
    return render(request, 'accounts/restDashboard.html')