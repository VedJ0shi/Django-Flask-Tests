from django.shortcuts import render
import datetime

# Create your views here.
def index(request):
    target = datetime.date(2025, 1, 1) #constructing date object represeting new year's day
    today = datetime.date.today() #class method that constructs date object representing today
    x = target - today #subtraction returns a timedelta object
    return render(request, "newyear/index.html", {"datematch":x == 0 , "daysleft":x.days})

