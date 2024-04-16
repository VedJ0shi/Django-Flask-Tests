from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import *


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
    
def profile(request, usname=None):
    if request.user.is_authenticated: #request.user attribute stores a validated instance of User model from django.contrib.auth.models
        if not usname or usname == request.user.username:
            if request.method == 'POST':
                usform = MyUpdateUserForm(request.POST, instance=request.user)
                prform = MyUpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
                if usform.is_valid and prform.is_valid:
                    usform.save()
                    prform.save()
                    return redirect('users-profile') #redirects as a GET request for same page (Post-Get redirect pattern)
            elif request.method == 'GET':
                usform = MyUpdateUserForm(instance=request.user)
                prform = MyUpdateProfileForm(instance=request.user.profile)
                count_posts = len(request.user.posts.all())
                friends = request.user.profile.friend.all()
                return render(request, 'users/profile.html', {'self':True, 'count': count_posts, 'friends': friends,
                                                          'usform': usform, 'prform': prform})
        else: 
            friend_user = User.objects.get(username=usname)
            count_posts = len(friend_user.posts.all())
            friends = friend_user.profile.friend.all()
            return render(request, 'users/profile.html', {'self':False, 'count': count_posts, 'friends': friends, 
                                                          'user': friend_user }) #overwrites user template variable
    else:
        return redirect('login') 