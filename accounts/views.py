# views.py
import json
from django.shortcuts import render, redirect

# from accounts.models import Profile
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, ReviewCreateForm
from .forms import FavoriteCreateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Review, Favorite
from .yelp_api import yelp_search
from .open_data_api import open_data_query
import os


def index(request):
    # #38
    cor_list = []
    context = {"google": os.environ.get("GOOGLE_API"), "location_list": cor_list}
    queryStr = request.GET
    if queryStr:
        params = {"location": queryStr.get("place"), "limit": 20}
        if not queryStr.get("place"):
            return render(request, "accounts/index.html", context=context)

        if queryStr.get("open_now"):
            params["open_now"] = True

        if queryStr.get("term"):
            params["term"] = queryStr.get("term")

        if queryStr.get("rating"):
            params["rating"] = queryStr.get("rating")

        if queryStr.get("price"):
            params["price"] = queryStr.get("price")

        search_object = yelp_search()
        result = search_object.filter_location(params)
        resultJSON = json.loads(result)

        for item in resultJSON["businesses"]:
            cor_list.append(
                {
                    "lat": item["coordinates"]["latitude"],
                    "lng": item["coordinates"]["longitude"],
                }
            )

        context = {
            "businesses": resultJSON["businesses"],
            "count": resultJSON["total"],
            "params": params,
            "google": os.environ.get("GOOGLE_API"),
            "location_list": cor_list,
        }

    return render(request, "accounts/index.html", context=context)


@login_required(login_url="login")
def locationDetail(request):
    if request.method == "GET":
        business_id = request.GET.get("locationID")
    elif request.method == "POST":
        business_id = request.POST.get("fav_locationid")
        if business_id:  # it is a adding favorite post
            if business_id[-1] == "/":
                business_id = business_id[:-1]
            print(business_id)
            business_name = request.POST.get("fav_locationname")
            favor_delete = Favorite.objects.filter(user=request.user,
                                                   yelp_id=business_id)
            if favor_delete:
                favor_delete.delete()
                messages.info(request, 'Unfavorite successfully')
            elif Favorite.objects.filter(user=request.user).count() >= 5:
                messages.info(request,
                              'Maximum of 5 favorited locations.' +
                              ' Please unfavorite one location before adding another.')
            else:
                form_dict = {
                    "user": request.user,
                    "yelp_id": business_id,
                    "business_name": business_name
                }
                form = FavoriteCreateForm(form_dict)
                if form.is_valid():
                    form.save()
                    print("Favorite object has been created successfully")

        else:  # it is a review post
            business_id = request.POST.get("locationid")
            if business_id[-1] == "/":
                business_id = business_id[:-1]

            review = request.POST.get("review")
            business_name = request.POST.get("locationname")
            wifi_rating = int(request.POST.get("wifi_rating"))
            comfort_rating = request.POST.get("comfort_rating")
            food_rating = request.POST.get("food_rating")
            charging_rating = request.POST.get("charging_rating")
            general_rating = request.POST.get("general_rating")
            post_user = request.user

            form_dict = {
                "user": post_user,
                "yelp_id": business_id,
                "business_name": business_name,
                "review_text": review,
                "wifi_rating": wifi_rating,
                "general_rating": general_rating,
                "food_rating": food_rating,
                "comfort_rating": comfort_rating,
                "charging_rating": charging_rating,
            }
            form = ReviewCreateForm(form_dict)

            if form.is_valid():
                form.save()
                print("Review form saved successfully")

    search_object = yelp_search()
    context = {}
    if business_id:
        review_list = Review.objects.filter(yelp_id=business_id).order_by(
            "-date_posted"
        )

        # get Yelp data
        yelp_result = search_object.search_business_id(business_id)
        resultJSON = json.loads(yelp_result)

        # open data query: pull name/zip/long/lat from Yelp data
        name = resultJSON["name"]
        zipcode = resultJSON["location"]["zip_code"]
        long_in = resultJSON["coordinates"]["longitude"]
        lat_in = resultJSON["coordinates"]["latitude"]

        # init open data query object, run sanitation/311 queries up init
        open_data_object = open_data_query(name, zipcode, long_in, lat_in)
        open_data_sanitation = json.loads(json.dumps(open_data_object.sanitation[0]))
        open_data_threeoneone = json.loads(json.dumps(open_data_object.three_one_one))
        # print(open_data_object.sanitation)
        favorite_list = Favorite.objects.filter(user=request.user, yelp_id=business_id)
        has_favorite = False
        if favorite_list.count() > 0:
            has_favorite = True

        context = {
            "business": resultJSON,
            "locationID": business_id,
            "reviews": review_list,
            "sanitation": open_data_sanitation,
            "three_one_one": open_data_threeoneone,
            "has_favorite": has_favorite
        }
    return render(request, "accounts/location_detail.html", context=context)


def registerPage(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # initialize profile
            user = form.cleaned_data.get("username")
            user_obj = User.objects.get(username=user)
            business_account = form.cleaned_data["business_account"]

            # ack business account creation
            if business_account:
                Profile.objects.filter(user=user_obj).update(business_account=True)
                # profile_obj = Profile.objects.get(user=user_obj)
                messages.success(
                    request, "Business account successfully created for " + user
                )
            else:
                messages.success(request, "Account successfully created for " + user)
            return redirect("login")

    return render(request, "accounts/register.html", {"form": form})


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("user")
        else:
            messages.info(request, "Username OR password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def user(request):
    return render(request, "accounts/user.html")


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    review_list = Review.objects.filter(user=request.user).order_by("-date_posted")
    favorite_list = Favorite.objects.filter(user=request.user).order_by("-date_posted")

    context = {
        "u_form": u_form,
        "p_form": p_form,
        "reviews": review_list,
        "favorites": favorite_list,
    }

    return render(request, "accounts/profile.html", context)
