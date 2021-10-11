# views.py
from django.shortcuts import render, redirect

from accounts.models import Profile
from .forms import RegisterForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "accounts/index.html")


def registerPage(request):
    form = RegisterForm()
    profile = Profile()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # initialize profile
            user = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            business_account = form.cleaned_data["business_account"]
            profile.set(user, email, business_account)
            profile.save()
            # ack business account creation
            if business_account == True:
                messages.success(request, "Business account successfully created for " + user)
            else:
                messages.success(request, "Account successfully created for " + user)
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
