from test2.models import *
from django.utils import timezone
from django.db import connection

loaded_restaurants = [{'name': 'Mings' , 'lat': 48.7, 'lon': 50.1, 'cuis': Restaurant.CuisineChoices.CHINESE},
                      {'name': 'Reddys', 'lat': 51.5 , 'lon': 54.0 , 'cuis': Restaurant.CuisineChoices.INDIAN},
                      {'name': 'Khans' , 'lat': 55.0, 'lon': 50.5, 'cuis': Restaurant.CuisineChoices.INDIAN},
                      {'name': 'Ernies', 'lat': 50.1, 'lon': 54.4, 'cuis': Restaurant.CuisineChoices.ITALIAN},
                      {'name': 'Taco Bell', 'lat': 48.5 , 'lon': 51.9 , 'cuis': Restaurant.CuisineChoices.AMERICAN}]

def run():
    '''creates Restaurant instances based on entries in loaded_restaurants list'''
    for entry in loaded_restaurants:
        restaurant = Restaurant()
        restaurant.name = entry.get('name')
        restaurant.latitude = entry.get('lat')
        restaurant.longitude = entry.get('lon')
        restaurant.date_opened = timezone.now()
        restaurant.cuisine = entry.get('cuis')
        restaurant.save() 

    print('sql query:',connection.queries)
    restaurants_in_db = Restaurant.objects.all()
    print(restaurants_in_db, len(restaurants_in_db))