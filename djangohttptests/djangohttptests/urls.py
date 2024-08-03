from django.contrib import admin
from django.urls import path, include
from cookies import views as cookies_views
from sessiondata import views as sessiondata_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cookies/', cookies_views.cookie),
    path('cookies/<slug:any>/', cookies_views.cookie),
    path('sessiondata/', sessiondata_views.visit)
]
