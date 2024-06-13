from django.shortcuts import render, redirect
from django.db import transaction
from .forms import *
import sys

# Create your views here.
def restock(request):
    if request.method == 'POST':
        form = ProductRestockForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('restock-product')     
    elif request.method == 'GET':
        form = ProductRestockForm()
        context = {'form': form, 'product_list': Product.objects.all()}
        return render(request, 'restock.html', context)
    

def simulate_SMS():
    print('Your order has been placed. Thank you!')

def order_product(request):
    if request.method == 'POST':
        form = ProductOrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                ordered = form.save() #if exception raised, then another user must have concurrently placed order on same product 
                ordered.product.number_in_stock = ordered.product.number_in_stock - ordered.number_of_items
                ordered.product.save(update_fields=['number_in_stock'])
            transaction.on_commit(simulate_SMS)
            return redirect('order-product')
        else:
            unclean_data = form.data
            return render(request,'order.html', {'form':form, 
                        'message':f'You attempted to order {unclean_data.get("number_of_items")} items'})

    elif request.method == 'GET':
        form = ProductOrderForm()
        context = {'form': form}
        return render(request, 'order.html', context)