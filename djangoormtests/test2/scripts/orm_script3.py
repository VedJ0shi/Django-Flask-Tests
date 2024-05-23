from django.contrib.auth.models import User
from django.utils import timezone
from ..models import *
import random

def run():
    '''creates random number of Sale instances per restaurant with random income values between 1-100'''
    restaurants = Restaurant.objects.all()
    for j in range(len(restaurants)):
        for _ in range(random.randint(1,6)):
            sold = random.uniform(1,100)
            Sale.objects.create(restaurant=restaurants[j],income=sold, datetime=timezone.now())