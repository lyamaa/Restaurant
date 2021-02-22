from django.db.models import fields
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed

from food.models import Restaurant, Food

class RestaurantSerializers(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'phone', 'address', 'logo')

    def get_logo(self, restaurant):
        request = self.context.get('request')
        logo_url = restaurant.logo.url
        return request.build_absolute_uri(logo_url)


class FoodSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Food
        fields = ("id", "name", "description", "image", "price")
    
    def get_image(self, food):
        request = self.context.get('request')
        image_url = food.image.url
        return request.build_absolute_uri(image_url)