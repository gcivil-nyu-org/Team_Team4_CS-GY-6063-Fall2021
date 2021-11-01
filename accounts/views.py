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
from .yelp_api import yelp_search
from .open_data_api import open_data_query
import os


def index(request):
    cor_list = []
    context = {"google": os.environ.get("GOOGLE_API"), "location_list": cor_list}
    queryStr = request.GET
    if queryStr:
        # hard coded search terms as cafe, restaurant, and study; 
        # narrows the scope of the returned applications in line with the value prop
        search_terms = 'cafe restaurant study'
        params = {'location': queryStr.get('place'), 'limit': 20, 'term': search_terms}
        params2 = {}
        if not queryStr.get('place'):
            return render(request, "accounts/index.html", context=context)

        if queryStr.get("open_now"):
            params["open_now"] = True

        if queryStr.get("rating"):
            params["rating"] = queryStr.get("rating")

        if queryStr.get('price'):
            params['price'] = queryStr.get('price')
 
        if queryStr.get('comfort'):
            params['comfort'] = queryStr.get('comfort')
            print("comfort", params['comfort'])

        # if queryStr.get('grade'):
        #     params2['grade'] = queryStr.get('grade')

        search_object = yelp_search()
        result = search_object.filter_location(params)
        resultJSON = json.loads(result)

        # loop over returned businesses and
        for index, item in enumerate(resultJSON['businesses']):

            long_in = item['coordinates']['longitude']
            lat_in = item['coordinates']['latitude']
            name = item['name']
            zipcode = item['location']['zip_code']

            cor_list.append(
                {'lat': item['coordinates']['latitude'], 'lng': item['coordinates']['longitude']})

            if queryStr.get('grade'):
                open_data_object = open_data_query(name, zipcode, long_in, lat_in)
                open_data_sanitation = open_data_object.sanitation
                                
                if (type(open_data_sanitation) is dict):
                    item['grade'] = open_data_sanitation['grade']
                else:
                    item['grade'] = ''

            if queryStr.get('311_check'):
                open_data_object = open_data_query(name, zipcode, long_in, lat_in)
                open_data_threeoneone = json.loads(
                json.dumps(open_data_object.three_one_one))

                # check whether 311 query returns, if yes render value
                if(open_data_threeoneone[0]['created_date'] == 'NA'):
                    item['check_311'] = True
                else:
                    item['check_311'] = False

            '''
            populate comfort parameter here...
            '''
            if queryStr.get('comfort'):
                try:
                    # define user rating param
                    rating_param = int(queryStr.get('comfort'))
                    # pull database object for location (i.e., item)
                    db_rating = Review.objects.filter(business_name=name)
                    # pull comfort_rating value from database object
                    db_rating = int(db_rating.values("comfort_rating")[0]['comfort_rating'])
                    if db_rating >= rating_param:
                        item['comfort'] = db_rating
                        print("comfort rating: ", item['comfort'])
                    else:
                        item['comfort'] = 0
                except:
                    item['comfort'] = 0
                                
        response = resultJSON['businesses']

        # functions used to filter results
        def filterByGrade(item):
            return item['grade'] == queryStr.get('grade')
    
        def filterBy311(item):
            if(item['check_311']):
                return True

        '''
        new comfort filter, referenced below.
        '''
        def filterByComfort(item):
            return int(item['comfort']) >= int(queryStr.get('comfort'))

        # conditionals to check on filter
        if queryStr.get('grade'):
            response = list(filter(filterByGrade, response))

        if queryStr.get('311_check'):
            response = list(filter(filterBy311, response))

        '''
        test comfort parameter here based on input...
        '''
        if queryStr.get('comfort'):
            response = list(filter(filterByComfort, response))

        
        context = {
            'businesses': response,
            'count': resultJSON['total'],
            'params': params,
            'google': os.environ.get('GOOGLE_API'),
            'location_list': cor_list
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

        # init open data query object, run sanitation/311 queries
        open_data_object = open_data_query(name, zipcode, long_in, lat_in)
        open_data_sanitation = open_data_object.sanitation
        open_data_threeoneone = open_data_object.three_one_one
        
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
