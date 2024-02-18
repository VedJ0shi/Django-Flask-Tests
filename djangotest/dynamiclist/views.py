from django.shortcuts import render

tasks = [] #dynamic list, global variable
# Create your views here.
def index(request):
    return render(request, "todo/index.html", {"tasks": tasks})

def add(request): #add is called either when going to url (GET) OR when submitting to the form (POST)
    if request.method == 'POST':
        task = request.POST["task"] #POST attribute contains POST variables as a dict
        tasks.append(task)  
    return render(request, "todo/form.html", {} )