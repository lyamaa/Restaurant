
from django.urls import path
from .views import RestaurantAPIView, CustomerGetFood, CustomerAddOrder, OrderNotify


urlpatterns = [
    path("customer/restaurant", RestaurantAPIView.as_view()),
    path("customer/meals/<str:restaurant_id>", CustomerGetFood.as_view()),
    path("customer/order/add", CustomerAddOrder.as_view()),
    path("restaurant/order/notification/<str:last_request_time>", OrderNotify.as_view() )
    # path("customer/order/latest", RestaurantAPIView.as_view()),

]
