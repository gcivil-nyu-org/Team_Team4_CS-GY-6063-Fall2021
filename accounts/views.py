# views.py
import json
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse

from accounts.models import Profile
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, ReviewCreateForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Review
from .yelp_api import yelp_search
import os


def index(request):
    # create yelp search object
    search_object = yelp_search()

    # example 1: query yelp API through search_location method
    yelp_term = 'cafe'
    yelp_location = 'New York City'
    search_object.search_location(yelp_term, yelp_location)

    # example 2: query yelp API through search_business_id method
    business_id = 'FEVQpbOPOwAPNIgO7D3xxw'
    search_object.search_business_id(business_id)

    # #38
    cor_list = []
    context = {'google': os.environ.get('GOOGLE_API'),
               'location_list': cor_list}
    queryStr = request.GET
    if queryStr:
        params = {'location': queryStr.get('place'), 'limit': 50}
        if not queryStr.get('place'):
            return render(request, "accounts/index.html", context=context)

        if queryStr.get('open_now'):
            params['open_now'] = True

        if queryStr.get('term'):
            params['term'] = queryStr.get('term')

        # if queryStr.get('category'):
        #     params['category'] = queryStr.get('category'),

        if queryStr.get('rating'):
            params['rating'] = queryStr.get('rating')

        if queryStr.get('price'):
            params['price'] = queryStr.get('price')

        result = search_object.filter_location(params)
        resultJSON = json.loads(result)

        for item in resultJSON['businesses']:
            cor_list.append(
                {'lat': item['coordinates']['latitude'], 'lng': item['coordinates']['longitude']})
        print(os.environ.get('GOOGLE_API'))

        context = {
            'businesses': resultJSON['businesses'],
            'count': resultJSON['total'],
            'params': params,
            'google': os.environ.get('GOOGLE_API'),
            'location_list': cor_list
        }

    return render(request, "accounts/index.html", context=context)


@login_required(login_url='login')
def locationDetail(request):
    if request.method == "GET":
        business_id = request.GET.get('locationID')

    elif request.method == "POST":
        business_id = request.POST.get('locationid')
        if business_id[-1] == '/':
            business_id = business_id[:-1]
        review = request.POST.get('review')
        business_name = request.POST.get('locationname')
        post_user = request.user
        form_dict = {'user': post_user, 'yelp_id': business_id,
                     'business_name': business_name, 'review_text': review}
        form = ReviewCreateForm(form_dict)
        if form.is_valid():
            form.save()
            print('form saved successfully')
    search_object = yelp_search()
    context = {}
    if business_id:
        review_list = Review.objects.filter(
            yelp_id=business_id).order_by('-date_posted')
        result = search_object.search_business_id(business_id)
        resultJSON = json.loads(result)
        context = {'business': resultJSON,
                   'locationID': business_id, 'reviews': review_list}
    return render(request, "accounts/location_detail.html", context=context)


def registerPage(request):
    form = RegisterForm()
    # profile = Profile()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # initialize profile
            user = form.cleaned_data.get("username")
            user_obj = User.objects.get(username=user)
            # email = form.cleaned_data.get("email")
            business_account = form.cleaned_data["business_account"]
            # profile.set(user, email, business_account)
            # profile.save()
            # ack business account creation
            if business_account:
                Profile.objects.filter(user=user_obj).update(
                    business_account=True)
                profile_obj = Profile.objects.get(user=user_obj)
                messages.success(
                    request, "Business account successfully created for " + user)
            else:
                messages.success(
                    request, "Account successfully created for " + user)
            return redirect("login")

    return render(request, "accounts/register.html", {"form": form})


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def user(request):
    return render(request, 'accounts/user.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    review_list = Review.objects.filter(
        user=request.user).order_by('-date_posted')
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'reviews': review_list
    }

    return render(request, 'accounts/profile.html', context)
