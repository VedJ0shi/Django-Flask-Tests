from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import *

class ProductStockException(Exception):
    pass

class NonexistentProductException(Exception):
    pass

class ProductOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields  = ('product', 'number_of_items')
    
    def save(self, commit=True):
        order_instance = super().save(commit=False)
        if order_instance.number_of_items > order_instance.product.number_in_stock:
            raise ProductStockException('This is now out of stock')
        else:
            if commit:
                super().save()
            return order_instance


class ProductRestockForm(forms.ModelForm):
    add_to_stock = forms.IntegerField(min_value=1)

    class Meta:
        model = Product
        fields  = ('name',)

    def save(self, commit=True):
        try:
            product_instance = Product.objects.get(name=self.cleaned_data['name'])
        except:
            raise NonexistentProductException('Not a listed product')
        product_instance.number_in_stock = product_instance.number_in_stock + self.cleaned_data['add_to_stock']
        if commit:
            product_instance.save(update_fields=['number_in_stock'])
        return product_instance

