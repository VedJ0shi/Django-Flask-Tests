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
            messages.success(request, f"Account created for {username}! You can now login.") #produces flash message
            return redirect('login') #'login' refers to the named route blog/login/
        
    elif request.method == "GET":
        form = MyRegistrationForm() #fresh form
        return render(request, 'users/register.html', {"form": form})
    
def profile(request, uname=None):
    if request.user.is_authenticated: #request.user attribute stores validated instance of User model from django.contrib.auth.models
        if not uname:
            count_posts = len(request.user.posts.all())
            friends = request.user.profile.friend.all()
            return render(request, 'users/profile.html', {'count': count_posts, 'friends': friends})
        else: 
            friend_user = User.objects.get(username=uname)
            count_posts = len(friend_user.posts.all())
            friends = friend_user.profile.friend.all()
            return render(request, 'users/profile.html', {'user': friend_user, 'count': count_posts, 'friends': friends}) #overrides user
    else:
        return redirect('login') 