from django.contrib import admin
from django.urls import path, include

from . import views   

urlpatterns = [
    path('login/',views.login, name="login"),
    path('login-submit',views.logging_in),
    path('signup', views.signup , name="signup"),
    path('signup',views.signup),
    path('signup_select',views.signup_select),
    path('signup_vol', views.signup_vol, name = "volunteerSign"),
    path('signup_submit',views.signup_submit),
    path('signup_submit',views.signup_submit),
    path('logout',views.logout),
    path('google',views.google),
    path('redirect',views.redirect),
]