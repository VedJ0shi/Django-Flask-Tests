from ..models import *
import random

def run():
    worker1, _ = Staff.objects.get_or_create(name='John Wick')
    worker2, _ = Staff.objects.get_or_create(name='Bob Dylan')
    worker3, _ = Staff.objects.get_or_create(name='Tom Brady')

    worker1.restaurants.add(Restaurant.objects.get(pk=random.randint(1,6)))

    worker2.restaurants.add(Restaurant.objects.get(pk=random.randint(1,6)), Restaurant.objects.get(pk=random.randint(1,6)))

    worker3.restaurants.set(Restaurant.objects.all()[0:3])
