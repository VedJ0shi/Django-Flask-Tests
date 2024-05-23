from django.contrib.auth.models import User
from test2.models import *
import random

def run():
    '''creates Rating instances with random number of stars between 2-5'''
    restaurants = Restaurant.objects.all()
    users = User.objects.all()
    for i in range(len(restaurants)):
        for j in range(len(users)):
            rated = random.randint(2,5)
            Rating.objects.create(user=users[j], restaurant=restaurants[i], stars=rated)
            print(f'{users[j]} rated {restaurants[i]} {rated} stars!')
            print()