from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
#auth.forms module contains several Form classes

# Create your views here.
def register(request):

    if request.method == "POST": #each HTTPRequest object contains "method" attribute
        form = MyRegistrationForm(request.POST) #form contains username and password data from form submission
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created! You can now login.") #produces flash message
            return redirect('login') #'login' refers to the named route blog/login/
        
    elif request.method == "GET":
        form = MyRegistrationForm() #fresh form
        return render(request, 'users/register.html', {"form": form})
    
def profile(request):
    if request.user.is_authenticated: #request.user attribute contains info about currently logged-in user
        return render(request, 'users/profile.html')
        #request.user stores a validated instance of User model class from django.contrib.auth.models
    else:
        return redirect('login') 