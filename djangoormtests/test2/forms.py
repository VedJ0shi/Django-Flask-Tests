from django import forms
from .models import *
from django.core.validators import EmailValidator #validator on Form field

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('user','restaurant','stars') #validation of 'stars' field/attribute will begin after .is_valid() called on Modelform instance

