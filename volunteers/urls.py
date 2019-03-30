from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
	
    path('vol_submit', views.vol_submit),

]