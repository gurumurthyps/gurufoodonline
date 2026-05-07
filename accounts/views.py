from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
# Create your views here.

def registerUser(request):
    if request.method=='POST':
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
    if request.method=='POST':
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
