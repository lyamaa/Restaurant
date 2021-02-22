from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.utils import timezone


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='restaurant_logo/', blank=False)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    avatar = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="food")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    image= models.ImageField(upload_to="foods_images/", blank=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "cooking"),
        (READY, "ready"),
        (ONTHEWAY, "on-the-way"),
        (DELIVERED, "delivered")
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) 
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255)
    total = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default= timezone.now)
    picked_at = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return str(self.id)



class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    sub_total = models.IntegerField()
    
    def __str__(self):
        return str(self.id)