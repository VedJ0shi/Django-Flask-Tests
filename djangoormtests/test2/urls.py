from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form, name='form'),
    path('stats/<slug:cname>/', views.stats, name='cstats'),
    path('stats/', views.stats, name='stats')
]
