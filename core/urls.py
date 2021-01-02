from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from food.views import register


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('food.urls')),
    path('register', register, name="register"),
    path('login', auth_views.LoginView.as_view(), {'template_name': 'registration/register.html'}, name="login"),
    path('auth/logout', auth_views.LogoutView.as_view(), {'next_page': '/'}, name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)