from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #2nd arg is the function that is called when url path is visited
    path('<str:user>', views.index),
    path('display/', views.display),
    path('display/<str:user>', views.display)
]