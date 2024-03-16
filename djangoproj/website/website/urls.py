from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/register/', users_views.register, name='users-register'), #will match url that exactly matches blog/register/ 
    path('blog/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login' ), 
    path('blog/logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout' ), #Login/Logout are Class-based views
    path('blog/profile/', users_views.profile, name='users-profile'),
    path('blog/', include('blog.urls')), #will match any url that begins with blog/ 
]
