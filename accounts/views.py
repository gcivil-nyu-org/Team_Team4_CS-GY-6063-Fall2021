# views.py
import json
from django.shortcuts import render, redirect
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, ReviewCreateForm
from .forms import FavoriteCreateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Review, Favorite
from django.db.models import Avg
from .yelp_api import Yelp_Search
from .open_data_api import open_data_query
from .zip_codes import filterInNYC, zipcodeInNYC, noNYCResults
from .filters import Checks, Filters
import os
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView


def review_update(request):
    return render(request, "accounts/review_update_suc.html")


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['review_text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.user:
            return True
        return False


def index(request):
    cor_list = []
    # params = {'limit': 20} 
    '''this seems redundant; should apply all of following before conditional'''
    # hard code search terms to narrow scope: cafe, restaurant, and study
    search_terms = 'cafe restaurant study'
    params = {'limit': 20, 'term': search_terms}
    context = {"google": os.environ.get("GOOGLE_API"), 
               "location_list": cor_list}
    queryStr = request.GET
    if queryStr:
        if not queryStr.get('place') and not queryStr.get('useCurrentLocation'):
            return render(request, "accounts/index.html", context=context)
        if queryStr.get('place'):
            params['location'] = queryStr.get('place')
        if queryStr.get('useCurrentLocation'):
            if queryStr.get('longitude') and queryStr.get('latitude'):
                params['longitude'] = queryStr.get('longitude')
                params['latitude'] = queryStr.get('latitude')
            elif not queryStr.get('place'):
                return render(request, "accounts/index.html", context=context)

        # pass user defined Yelp! params to Yelp API
        if queryStr.get('open_now'):
            params['open_now'] = True

        if queryStr.get('price'):
            params['price'] = queryStr.get('price')

        search_object = Yelp_Search()
        result = search_object.filter_location(params)

        # exception handling for invalid search terms
        invalid_search = False
        try: 
            resultJSON = json.loads(result)
        except TypeError:
            invalid_search = True
            context = {
                'businesses': [],
                'count': 0,
                'params': params,
                'google': os.environ.get('GOOGLE_API'),
                'location_list': cor_list,
                'invalid_search': invalid_search,
                'recommendations': []
            }
            return render(request, "accounts/index.html", context=context)

        # loop over returned businesses and update items from database 
        for index, item in enumerate(resultJSON['businesses']):
            #name = item['name'] used in 311
            zipcode = item['location']['zip_code']
            zipcodeInNYC(item, zipcode)

            cor_list.append(
                {'lat': item['coordinates']['latitude'], 'lng': item['coordinates']['longitude']})

            # update search object with user defined filter
            check_query = Checks(item, 
                                 queryStr.get('comfort'),
                                 queryStr.get('food'),
                                 queryStr.get('wifi'),
                                 queryStr.get('charging')
                                 #queryStr.get('311_check')
                                 )

            check_query.perform_checks()

        response = resultJSON['businesses']
        # filter for locations outside of NYC 
        response = list(filter(filterInNYC, response))
        # if response is empty, also consider search invalid
        invalid_search = noNYCResults(response)
        # save copy to provide recommended results
        unfiltered_response = response

        # filter results based on user input
        filter_results = Filters(response,
                          queryStr.get('comfort'),
                          queryStr.get('food'),
                          queryStr.get('wifi'),
                          queryStr.get('charging'),
                          queryStr.get('rating')
                          #queryStr.get('311_check')
                          )

        response = filter_results.filter_all()

        # if the filter returns less than 3 locations, provided suggestions
        recommendations = [i for i in unfiltered_response if i not in response] if len(response) < 3 else []

        context = {
            'businesses': response,
            'count': resultJSON['total'],
            'params': params,
            'google': os.environ.get('GOOGLE_API'),
            'location_list': cor_list,
            'recommendations': recommendations,
            'invalid_search': invalid_search
        }

    return render(request, "accounts/index.html", context=context)


@login_required(login_url='login')
def locationDetail(request):
    if request.method == "GET":
        business_id = request.GET.get("locationID")
    elif request.method == "POST":
        business_id = request.POST.get("fav_locationid")
        if business_id:  # it is a adding favorite post
            business_name = request.POST.get("fav_locationname")
            favor_delete = Favorite.objects.filter(user=request.user,
                                                   yelp_id=business_id)
            if favor_delete:
                favor_delete.delete()
                messages.info(request, 'Unfavorite successfully!')
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
                    messages.info(request, 'Favorite successfully!')
                    print("Favorite object has been created successfully")

        else:  # it is a review post
            business_id = request.POST.get("locationid")
            review = request.POST.get("review")
            business_name = request.POST.get("locationname")
            wifi_rating = int(request.POST.get("wifi_rating"))
            comfort_rating = request.POST.get("comfort_rating")
            food_rating = request.POST.get("food_rating")
            charging_rating = request.POST.get("charging_rating")
            general_rating = request.POST.get("general_rating")
            post_user = request.user
            Review.objects.filter(user=post_user, )
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
            previous_review = Review.objects.filter(user=post_user, yelp_id=business_id)
            # previous_review.delete()
            if previous_review:
                previous_review.delete()
                messages.info(request,
                              'The new review is posted' +
                              ' and your earlier review is deleted.')
            else:
                messages.info(request,
                              'Your review is posted')
            if form.is_valid():
                form.save()
                print("Review form saved successfully")
            else:
                print("Review form is invalid")

    search_object = Yelp_Search()
    context = {}
    if business_id:
        review_list = Review.objects.filter(yelp_id=business_id).order_by(
            "-date_posted"
        )
        avg_field_list = ['wifi_rating', 'general_rating',
                          'food_rating', 'comfort_rating', 'charging_rating']
        avg_dict = dict()
        for field_name in avg_field_list:
            avg_dict.update(Review.objects.filter(
                yelp_id=business_id).aggregate(Avg(field_name)))
        for x in avg_dict:
            if avg_dict[x] is None:
                avg_dict[x] = '-'
            else:
                avg_dict[x] = round(avg_dict[x], 1)

        # get Yelp data
        yelp_result = search_object.search_business_id(business_id)
        resultJSON = json.loads(yelp_result)

        # open data query: pull name/zip/long/lat from Yelp data
        name = resultJSON["name"]
        zipcode = resultJSON["location"]["zip_code"]
        long_in = resultJSON["coordinates"]["longitude"]
        lat_in = resultJSON["coordinates"]["latitude"]

        # init open data query object, run sanitation/311 queries
        open_data_object = open_data_query(name, zipcode, long_in, lat_in)
        open_data_sanitation = open_data_object.sanitation
        open_data_threeoneone = open_data_object.three_one_one

        favorite_list = Favorite.objects.filter(user=request.user, yelp_id=business_id)
        has_favorite = False
        if favorite_list.count() > 0:
            has_favorite = True

        # check if the user is a business account
        is_business = Profile.objects.get(user=request.user).business_account

        # check if location is verified
        try:
            is_verified = Profile.objects.filter(verified_yelp_id=business_id).values('verified')[0]['verified']
        except IndexError:
            is_verified = False

        context = {
            "business": resultJSON,
            "locationID": business_id,
            "reviews": review_list,
            "sanitation": open_data_sanitation,
            "three_one_one": open_data_threeoneone,
            "has_favorite": has_favorite,
            "avg_dict": avg_dict,
            "is_business": is_business,
            "is_verified": is_verified
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
            return redirect("index")
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
