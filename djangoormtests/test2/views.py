from django.shortcuts import render, redirect
from django.db.models import Prefetch
from .forms import *
from .models import *

# Create your views here.
def index(request):
    context = {}
    restaurants = Restaurant.objects.prefetch_related('ratings') #caches all related objects for each of the instances in retrieved QuerySet
    context['restaurants'] = restaurants
    return render(request, 'index.html', context)

def stats(request, cname=None):
    context = {}
    if cname==None:
        sales = Sale.objects.select_related('restaurant') #executes JOIN on Sale and Restaurant table and caches result
        context['sales'] = sales
        return render(request, 'stats.html', context)
    else:
        top_sales = Prefetch('sales', queryset=Sale.objects.filter(income__gte=60)) #first arg is the lookup in related model
        try:
            restaurants = Restaurant.objects.filter(cuisine__iexact=cname).prefetch_related(top_sales)
        except:
            return render(request, 'stats.html', context)
        else:
            context['restaurants'] = restaurants
        return render(request, 'cuisine_stats.html', context)


def form(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid(): #triggers modelform validation routines (including .full_clean() on model instance)
            form.save() #saves downstream Rating instance to database
            request.session['message'] = f'Success- Saved rating of {form.cleaned_data["stars"]} for {form.cleaned_data["restaurant"]}'
        else:
            error = f'Error- You attempted to rate {Restaurant.objects.get(pk=form.data["restaurant"])} with {form.data["stars"]} stars. Please limit your rating to between 1 and 5'
            request.session['message'] = error
        return redirect('form')
    elif request.method == 'GET':
        form = RatingForm()
        return render(request, 'form.html', {'form': form })
    
