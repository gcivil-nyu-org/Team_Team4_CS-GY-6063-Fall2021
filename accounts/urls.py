from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.user, name="user"),
    path('profile/', views.profile, name="profile"),
    path('location', views.locationDetail, name="locationDetail"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
