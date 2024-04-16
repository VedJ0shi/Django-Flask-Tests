from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/register/', users_views.register, name='users-register'), 
    path('blog/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login' ), 
    path('blog/logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout' ), #Login/Logout are Class-based views
    path('blog/profile/', users_views.profile, name='users-profile'),
    path('blog/profile/<str:usname>', users_views.profile, name='users-profile-x'),
    path('blog/', include('blog.urls')), #will match any url that begins with blog/ 
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)