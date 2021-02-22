from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Food, Order
from food.forms import FoodForm, UserForm, RestaurantForm, UserEditForm

from django.core.exceptions import ObjectDoesNotExist



@login_required(login_url="/login")
def home(request):
    return render(request, 'home.html', {})
    # return redirect(restaurant_order)


@login_required(login_url="/login")
def restaurant_account(request):
    user_edit_form = UserEditForm(instance=request.user)
    restaurant_edit_form = RestaurantForm(instance = request.user.restaurant)

    try:
        if request.method == "POST":
            user_edit_form = UserEditForm(request.POST, instance = request.user)
            restaurant_edit_form = RestaurantForm(request.POST, request.FILES, instance = request.user.restaurant)

            if user_edit_form.is_valid and restaurant_edit_form.is_valid():
                user_edit_form.save()
                restaurant_edit_form.save()
    except ObjectDoesNotExist:
        print("There is no restaurant here.")
        return redirect(home)

    # if request.method == "POST":
    #     user_edit_form = UserEditForm(request.POST, instance = request.user)
    #     restaurant_edit_form = RestaurantForm(request.POST, request.FILES, instance = request.user.restaurant)

    #     if user_edit_form.is_valid and restaurant_edit_form.is_valid():
    #         user_edit_form.save()
    #         restaurant_edit_form.save()

    return render(request, 'restaurant/account.html', {"user_edit_form": user_edit_form, "restaurant_edit_form": restaurant_edit_form})


@login_required(login_url="/login")
def restaurant_meal(request):
    foods = Food.objects.filter(restaurant = request.user.restaurant).order_by("-id")
    return render(request, 'restaurant/meal.html', {"foods": foods})


@login_required(login_url="/login")
def restaurant_add_meal(request):
    form = FoodForm()
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)

        if form.is_valid():
            food = form.save(commit=False)
            food.restaurant = request.user.restaurant
            food.save()
            return redirect(restaurant_meal)
    return render(request, 'restaurant/add_meal.html', {"form": form})


@login_required(login_url="/login")
def restaurant_edit_meal(request, food_id):
    form = FoodForm(instance=Food.objects.get(id=food_id))
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES, instance= Food.objects.get(id=food_id))

        if form.is_valid():
            form.save()
            return redirect(restaurant_meal)
    return render(request, 'restaurant/edit_meal.html', {"form": form})


@login_required(login_url="/login")
def restaurant_order(request):
    if request.method == "POST":
        order = Order.objects.get(id= request.POST["id"], restaurant = request.user.restaurant)

        if order.status == Order.COOKING:
            order.status = Order.READY
            order.save()
    orders = Order.objects.filter(restaurant = request.user.restaurant).order_by("-id")
    return render(request, 'restaurant/order.html', {"orders": orders})


@login_required(login_url="/login")
def restaurant_report(request):
    return render(request, 'restaurant/report.html', {})


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
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password']
            ))

            return redirect(home)

    return render(request, 'registration/register.html', {
        "user_form": user_form,
        "restaurant_form ": restaurant_form
    })

