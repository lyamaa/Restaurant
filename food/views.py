from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from food.forms import UserForm, RestaurantForm

@login_required(login_url="/login")
def home(request):
    return render(request, 'home.html', {})


def register(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()
    if request.method == "POST":
        user_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)

        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()

            login(request, authenticate(
                username = user_form.cleaned_data['username'],
                password = user_form.cleaned_data['password']
            ))

            return redirect(home)


    return render(request, 'registration/register.html', {
        "user_form": user_form,
        "restaurant_form ": restaurant_form
    })