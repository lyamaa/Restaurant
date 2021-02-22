from django import forms

from django.contrib.auth.models import User

from food.models import Food, Restaurant


class UserForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, required=True)
    password =forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, required=True)
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("name", "phone", "address", "logo")


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = ("restaurant",)