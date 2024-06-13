from django.urls import path
from . import views

urlpatterns = [
    path('', views.restock, name='restock-product'),
    path('order/', views.order_product, name='order-product')
]
