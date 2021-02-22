import django
from django.db.models.deletion import SET_DEFAULT
from rest_framework import serializers
from django.utils import timezone
from oauth2_provider.models import AccessToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import FoodSerializer, RestaurantSerializers
from food.models import Restaurant, Food, Order, OrderDetail

import json


class RestaurantAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RestaurantSerializers(
            Restaurant.objects.all(), many=True, context={"request": request})

        return Response(serializer.data)

# Get List of food by specific restaurant


class CustomerGetFood(APIView):

    def get(self, request, restaurant_id):
        foods = FoodSerializer(
            Food.objects.filter(restaurant_id=restaurant_id).order_by("-id"),
            many=True, context={"request": request}
        )
        return Response(foods.data)


class CustomerAddOrder(APIView):

    def post(self, request):
        if request.method == "POST":
            access_token = AccessToken.objects.get(
                token=request.POST.get("access_token"), expires__gt=timezone.now())
            customer = access_token.user.customer

            if Order.objects.filter(customer=customer).exclude(status=Order.DELIVERED):
                return Response({"status": "Fail", "error": "Your last order must be completed."})

            # Check address
            if not request.POST["address"]:
                return Response({"status": "failed", "error": "Address is required"})

            order_details = json.loads(request.POST["order_details"])
            order_total = 0
            for food in order_details:
                order_total += Food.objects.get(
                    id=food["food_id"]).price * food["quantity"]

            if len(order_details) > 0:
                order = Order.objects.create(
                    customer=customer,
                    restaurant_id=request.POST["restaurant_id"],
                    total=order_total,
                    status=Order.COOKING,
                    address=request.POST["address"]
                )

                for food in order_details:
                    OrderDetail.objects.create(
                        order=order,
                        food_id=food["food_id"],
                        quantity=food["quantity"],
                        sub_total=Food.objects.get(
                            id=food["food_id"]).price * food["quantity"]
                    )

                    return Response({"status": "success"})


class CustomerGetLatestOrder(APIView):

    pass


class OrderNotify(APIView):
    def get(request, last_request_time):
        notification = Order.objects.filter(
            restaurant=request.user.restaurant, created_at__gt=last_request_time).count()
        
        return Response({notification.data})