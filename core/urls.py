from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from food.views import (
    register,
    restaurant_account,
    restaurant_meal,
    restaurant_add_meal,
    restaurant_edit_meal,
    restaurant_order,
    restaurant_report
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('food.urls')),
    path('api/', include('food.api.urls')),
    path('register', register, name="register"),
    path('login', auth_views.LoginView.as_view(), {
         'template_name': 'registration/register.html'}, name="login"),
    path('auth/logout', auth_views.LogoutView.as_view(),
         {'next_page': '/'}, name="logout"),
    re_path(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    path('restaurant/account/', restaurant_account, name='restaurant-account'),
    path('restaurant/meal/', restaurant_meal, name='restaurant-meal'),
    path('restaurant/meal/add', restaurant_add_meal, name='restaurant-meal-add'),
    path('restaurant/meal/<str:food_id>',
         restaurant_edit_meal, name='restaurant-meal-edit'),
    path('restaurant/order/', restaurant_order, name='restaurant-order'),
    path('restaurant/report/', restaurant_report, name='restaurant-report'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
