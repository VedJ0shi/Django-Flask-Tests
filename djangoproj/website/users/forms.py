from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

'''ModelForm provides functionality for username creation;
it's subclass UserCreationForm provides password functionality'''

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User #specifies the model this interacts with i.e. .save() will be applied to User.objects.all()
        fields = ['username', 'email', 'password1', 'password2'] #password2 refers to password confirmation


class MyUpdateUserForm(forms.ModelForm):
    '''to update username and email only'''
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['username', 'email']


class MyUpdateProfileForm(forms.ModelForm):
    '''to update profile pic only'''
    class Meta:
        model = Profile
        fields = ['profpic']
