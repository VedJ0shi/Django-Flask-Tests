from django.db import models

'''each model (i.e. Airport, Flight) is a custom subclass of the models.Model class 
and maps to a db table'''

''' model fields (i.e. code, city, origin, etc [columns of the table]) are set up as class 
attributes of the model, and each field stores the instance/object of an appropriate
Field class (i.e. CharField, BooleanField, etc - defined in the imported models module)
 '''

'''a row of the table is an instance of the corresponding model'''

#https://docs.djangoproject.com/en/5.0/ref/models/fields/#field-types

# Create your models here.
class Airport(models.Model): 
    '''each row in the Airport table will be an instance/object of this Class-- 
    of type flights.models.Airport'''
    code = models.CharField(max_length=3, unique=True)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    '''each row in the Flight table will be an instance/object of this Class-- 
    of type flights.models.Flight'''
    origin = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="arrivals") 
    duration = models.IntegerField()
    is_full = models.BooleanField()

    def __str__(self):
        return f"{self.origin}-->{self.destination}"