from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ReviewUpdateView, ReviewDeleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('bz_update/', views.bz_update),
    path('', views.index, name='index'),
    path('register/', views.registerPage, name="register"),

    path('login/', auth_views.LoginView.as_view(
        template_name="accounts/login.html"), name="login"),
    # path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('location', views.locationDetail, name="locationDetail"),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('review/update/successful', views.review_update, name='review-update-suc'),
    path('review/delete/successful', views.review_delete, name='review-delete-suc'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount, name='activate'),
    path('about/', views.about, name='about'),
    path('checkout/', views.create_checkout_session,
         name='create_checkout_session'),
    path('checkout-success/', views.checkout_success, name="checkout_success"),
    path('checkout-cancel/', views.checkout_cancel, name="checkout_cancel"),
    path('advertise/', views.advertise, name='advertise'),
    path('webhook/', views.webhook_view, name='webhook_view'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
