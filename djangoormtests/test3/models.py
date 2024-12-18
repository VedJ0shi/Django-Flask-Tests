from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
        

class Product(models.Model):
    name = models.CharField(max_length=100)
    number_in_stock = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name



class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_items = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.number_of_items} x {self.product.name}'

    def clean(self):
        if self.number_of_items > self.product.number_in_stock:
            raise ValidationError('Order exceeded stock')
            

