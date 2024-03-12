from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
#auth.forms module contains several Form classes

# Create your views here.
def register(request):

    if request.method == "POST": #each HTTPRequest object contains "method" attribute
        form = MyRegistrationForm(request.POST) #form contains username and password data from form submission
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created, welcome {username}") #produces flash message
            return redirect('blog-home') #'blog-home' is the named url route that calls blog.views.home
        
    elif request.method == "GET":
        form = MyRegistrationForm() #fresh form
    return render(request, 'users/register.html', {"form": form})