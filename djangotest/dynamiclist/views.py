from django.shortcuts import render

tasks = ["foo", "bar", "baz"] #dynamic list
# Create your views here.
def index(request):
    return render(request, "todo/index.html", {"tasks": tasks})

def add(request):
    return render(request, "todo/form.html", {} )