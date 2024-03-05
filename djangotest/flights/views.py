from django.shortcuts import render
from .models import Flight, Airport

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {"flights": Flight.objects.all()})
    #objects.all() returns a QuerySet, an iterable of created Flight objects (rows in table)
