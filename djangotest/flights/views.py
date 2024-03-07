from django.shortcuts import render
from .models import Flight, Passenger #imports model/class

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {"flights": Flight.objects.all()})
    #objects.all() returns a QuerySet, an iterable of created Flight objects (rows in table)

def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id) #pk refers to 'primary key'
    #flight is a Flight instance (corresponding to a table row)
    return render(request, "flights/flight.html", {"flight":flight, "passengers":flight.passengers.all()})
