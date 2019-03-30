from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
	
    path('school_submit', views.school_submit),
    path('',views.index)


]