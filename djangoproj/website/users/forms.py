from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User #specifies the model this interacts with i.e. .save() will be applied to User.objects.all()
        fields = ['username', 'email', 'password1', 'password2'] #password2 refers to password confirmation
