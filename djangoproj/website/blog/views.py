from django.shortcuts import render
from .models import * #imports Blogpost model class

# Create your views here.
def home(request):
    #return HttpResponse('<h1>Blog Homepage</h1>')
    return render(request, 'blog/home.html', {'posts': Blogpost.objects.all()}) #passing in QuerySet of Blogpost model objects (table rows)

def about(request, date):
    return render(request, 'blog/about.html', {"today": f"{date.month}/{date.day}"})