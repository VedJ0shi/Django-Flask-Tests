from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="blog-home"), #3rd arg is name of the url route
    path('about/', views.about, name="blog-about")
]