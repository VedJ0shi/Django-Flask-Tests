from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request, user="visitor"):
    return HttpResponse(f"Hello {user.capitalize()}, welcome friend")

def display(request, user="visitor"):
    return render(request, "hello/display.html", {"name":user.capitalize()}) #2nd arg is filename of template
