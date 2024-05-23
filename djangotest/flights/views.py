from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Airport, Flight, Passenger #imports model/class

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "flights/index.html", {"flights": Flight.objects.all(), "airports": Airport.objects.all()})
        #objects.all() returns a QuerySet-- an iterable of created model objects (different rows in table)
    elif request.method == "POST": 
        '''adds new flight based on form submission'''
        rq = request.POST #rq is simply an alias for dict returned by request.POST 
        origin_code, destination_code, duration = (rq["origin"], rq["destination"], rq["duration"])
        origin_obj = Airport.objects.get(code=origin_code)
        destination_obj = Airport.objects.get(code=destination_code)
        Flight.objects.create(origin=origin_obj, destination=destination_obj, duration=int(duration), is_full=False)
        return render(request, "flights/index.html", {"flights": Flight.objects.all(), "airports": Airport.objects.all()})

def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id) #pk refers to 'primary key'
    #flight is a Flight object, a member of QuerySet returned by Flight.objects.all()
    return render(request, "flights/flight.html", {
        "flight":flight, "passengers":flight.passengers.all(), 
        "non_passengers":Passenger.objects.exclude(flights=flight).all()})

def book(request, flight_id, auth):
    if auth == 1: 
        if request.method == "POST": 
            '''adds a flight to a passenger based on form submission'''
            flight = Flight.objects.get(pk=flight_id) #retrieve correct Flight object
            passenger = Passenger.objects.get(name=request.POST['passenger']) #retrieve correct Passenger object corresponding to form submission
            passenger.flights.add(flight) #augments passenger.flights.all() QuerySet
            return HttpResponseRedirect(reverse(('flights-flight'), args=(flight.id,))) #reloads flight page


    else:
        return HttpResponse('user not authenticated')
