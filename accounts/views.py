# views.py
import json
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, ReviewCreateForm
from .forms import BusinessUpdate, BusinessProfileForm
from .forms import FavoriteCreateForm
from django.contrib.auth import logout
# from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Review, Favorite, BProfile
from django.db.models import Avg
from .yelp_api import Yelp_Search
from .open_data_api import Open_Data_Query
from .zip_codes import filterInNYC, zipcodeInNYC, noNYCResults
from .filters import Checks, Filters
from .advertising import AdClients
import os
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from dateutil.relativedelta import relativedelta
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET')
YOUR_DOMAIN = os.environ.get('DOMAIN')


@csrf_exempt
def webhook_view(request):
    payload = request.body
    event = None
    plans = {"9990": 12, "3990": 3, "1990": 1}
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'charge.succeeded':
        user_email = event.data.object.billing_details.email
        price = str(event.data.object.amount)
        user = User.objects.get(email=user_email)
        if user:
            bprofile = BProfile.objects.get(user=user)
            bprofile.is_promoted = True
            currDate = date.today()
            bprofile.promote_start_date = currDate
            if price in plans:
                bprofile.promote_end_date = currDate + \
                    relativedelta(months=plans[price])
            bprofile.save()
    # else:
    #     print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


def advertise(request):
    items = {"1": "price_1K2iIXEYo8rGfFwcIkRtJkJi",
             "2": "price_1K2iI7EYo8rGfFwc91I2y65L", "3": "price_1K2iJfEYo8rGfFwcvJcaxc5m"}
    context = {}
    user = Profile.objects.get(user=request.user)
    if user:
        is_business = user.business_account
        is_verified = user.verified
        context = {"is_business": is_business, "is_verified": is_verified}
    try:
        business_profile = BProfile.objects.get(user=request.user)
        context["is_promoted"] = business_profile.is_promoted
        context["promote_end_date"] = business_profile.promote_end_date
    except Exception:
        business_profile = None

    if request.method == "POST":
        plan = request.POST.get('plan')
        if plan:
            line_items = [{"price": items[plan], "quantity": 1}]
            return create_checkout_session(line_items)
    return render(request, "accounts/advertise.html", context)


def checkout_success(request):
    return render(request, "accounts/checkout_success.html")


def checkout_cancel(request):
    return render(request, "accounts/checkout_cancel.html")


def create_checkout_session(line_items):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/checkout-success',
            cancel_url=YOUR_DOMAIN + '/checkout-cancel',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url)


def bz_update(request):
    if request.method == "POST":
        # bform = BusinessUpdate(request.POST, instance=request.user.bprofile)
        bform = BusinessUpdate(request.POST, request.FILES,
                               instance=request.user.bprofile)
        if bform.is_valid():
            bform.save()
            return render(request, "accounts/business_info_update_suc.html")
    bform = BusinessUpdate(instance=request.user.bprofile)
    context = {
        "bform": bform
    }
    return render(request, "accounts/bz_update.html", context)


def review_update(request):
    return render(request, "accounts/review_update_suc.html")


def review_delete(request):
    return render(request, "accounts/review_delete_suc.html")


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    # success_url = reverse('review-delete-suc')
    # sucess

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.user:
            return True
        return False

    def get_success_url(self):
        return reverse('review-delete-suc')


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
            return redirect('index')
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

        # loop over returned businesses, update items with database info
        for index, item in enumerate(resultJSON['businesses']):
            zipcode = item['location']['zip_code']
            zipcodeInNYC(item, zipcode)

            # update search object with user defined filter
            check_query = Checks(item,
                                 queryStr.get('comfort'),
                                 queryStr.get('food'),
                                 queryStr.get('wifi'),
                                 queryStr.get('charging'),
                                 queryStr.get('311_check')
                                 )

            check_query.perform_checks()
            
            # add tag to response for locations that are advertising
            ad_clients = AdClients(item)

            ad_clients.check_if_advertising()

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
                                 queryStr.get('rating'),
                                 queryStr.get('311_check')
                                 )

        response = filter_results.filter_all()

        # sort response list by if business is advertising
        response = sorted(response, 
                        key=lambda item: item['advertising'], 
                        reverse=True)

        # if the filter returns < 3 locations, provided suggestions
        recommendations = [i for i in unfiltered_response if i not in response] if len(
            response) < 3 else []

        # create coordinate list post filtering, add labels for map
        labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for index, item in enumerate(response):
            item['label'] = labels[index]
            cor_list.append({'id': item['id'],
                             'name': item['name'],
                             'lat': item['coordinates']['latitude'],
                             'lng': item['coordinates']['longitude'],
                             'label': item['label']})

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

            if request.POST.get("unfavorite"):
                favor_delete = Favorite.objects.filter(user=request.user,
                                                       yelp_id=business_id)
                # if favor_delete:
                favor_delete.delete()
                messages.info(request, 'Unfavorite successfully!')
            elif Favorite.objects.filter(user=request.user).count() >= 5:
                messages.info(request,
                              'Maximum of 5 favorited locations.' +
                              ' Please unfavorite one location before adding another.')
            else:
                favor_ = Favorite.objects.filter(user=request.user,
                                                 yelp_id=business_id)
                if not favor_:
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
        return redirect(reverse('locationDetail')+'?locationID='+business_id)
        # return redirect(reverse())

    search_object = Yelp_Search()
    context = {}
    if business_id:
        review_list = Review.objects.filter(yelp_id=business_id, review_text__gt='').order_by(
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
                avg_dict[x] = -1
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
        open_data_object = Open_Data_Query(name, zipcode, long_in, lat_in)
        open_data_sanitation = open_data_object.sanitation
        open_data_threeoneone = open_data_object.three_one_one

        favorite_list = Favorite.objects.filter(user=request.user, yelp_id=business_id)
        has_favorite = False
        if favorite_list.count() > 0:
            has_favorite = True

        # check if the user is a business account
        is_business = Profile.objects.get(user=request.user).business_account
        is_owner = Profile.objects.filter(
            user=request.user, verified_yelp_id=business_id).count() == 1
        # check if location is verified
        try:
            is_verified = Profile.objects.filter(
                verified_yelp_id=business_id).values('verified')[0]['verified']
        except IndexError:
            is_verified = False

        info = None
        if is_verified:

            profile = Profile.objects.filter(verified_yelp_id=business_id)
            if profile.count() == 1:
                user_ = profile[0].user
                bp = BProfile.objects.filter(user=user_)
                if bp.count() == 1:
                    info = bp[0]

        userReviewExists = False
        for review in review_list:
            if review.user == request.user:
                userReviewExists = True

        context = {
            "business": resultJSON,
            "locationID": business_id,
            "reviews": review_list,
            "sanitation": open_data_sanitation,
            "three_one_one": open_data_threeoneone,
            "has_favorite": has_favorite,
            "avg_dict": avg_dict,
            "is_business": is_business,
            "is_verified": is_verified,
            "is_owner": is_owner,
            'google': os.environ.get('GOOGLE_API'),
            "business_info": info,
            "userReviewExists": userReviewExists,
        }

    return render(request, "accounts/location_detail.html", context=context)


def registerPage(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            createdUser = form.save(commit=False)
            createdUser.is_active = False
            createdUser.save()
            # initialize profile
            user = form.cleaned_data.get("username")
            user_obj = User.objects.get(username=user)
            business_account = form.cleaned_data["business_account"]

            # ack business account creation
            if business_account:
                Profile.objects.filter(user=user_obj).update(business_account=True)
                bdict = {
                    "user": user_obj
                }
                bzform = BusinessProfileForm(bdict)
                if bzform.is_valid():
                    bzform.save()
                    print("Bzforn created")
                # messages.success(
                #     request, "Business account successfully created for " + user
                # )
            else:
                # messages.success(request, "Account successfully created for " + user)
                pass

            # send email
            current_site = get_current_site(request)
            subject = 'Activate Your StudyCity Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': createdUser,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(createdUser.pk)),
                'token': account_activation_token.make_token(createdUser),
            })
            createdUser.email_user(subject, message)
            messages.success(
                request, ('Please confirm your email to complete registration.'))
            return redirect("login")

    return render(request, "accounts/register.html", {"form": form})


def ActivateAccount(request, uidb64, token, *args, **kwargs):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if not account_activation_token.check_token(user, token):
            return redirect('login'+'?message='+'User already activated')

        if user.is_active:
            return redirect('login')
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()

        messages.success(request, 'Account activated successfully')
        return redirect('login')

    except Exception:
        pass

    return redirect('login')


# def loginPage(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             print(request.get_full_path())
#             print("url: ", request.GET.get("next"))
#             next_url = request.GET.get("next")
#             if next_url:
#                 return redirect(next_url)
#             else:
#                 return redirect("index")
#         else:
#             messages.info(request, "Username OR password is incorrect")

#     context = {}
#     return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    if request.method == "POST" and not request.POST.get('remove_image'):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("profile")
    elif request.method == "POST" and request.POST.get('remove_image'):
        Profile.objects.filter(user=request.user).update(
            image="profile_pics/default.jpg")
        return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    review_list = Review.objects.filter(user=request.user).order_by("-date_posted")
    favorite_list = Favorite.objects.filter(user=request.user).order_by("-date_posted")

    search_object = Yelp_Search()
    new_list = []
    for favorite in favorite_list:
        data = search_object.search_business_id(favorite.yelp_id)
        resultJSON = json.loads(data)
        new_list.append(
            {"name": favorite.business_name,
             "yelp_id": favorite.yelp_id, "img_url": resultJSON['image_url']})

    context = {
        "u_form": u_form,
        "p_form": p_form,
        "reviews": review_list,
        "favorites": new_list,
    }

    return render(request, "accounts/profile.html", context)


def about(request):
    return render(request, "accounts/about.html")
