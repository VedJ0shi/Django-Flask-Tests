from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="flights-index"),
    path("<int:flight_id>/", views.flight, name="flights-flight"),
    path("<int:flight_id>/book/", views.book, {"auth": 1}, name="flights-book")
]