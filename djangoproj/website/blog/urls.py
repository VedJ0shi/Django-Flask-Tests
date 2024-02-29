from django.urls import path
from . import views
import datetime


urlpatterns = [
    path('', views.home, name="blog-home"), #name arg is reference name of the url route
    path('about/', views.about, {"date": datetime.date.today()}, name="blog-about") #optional 3rd arg is keyword arg(s) passed to view function
]