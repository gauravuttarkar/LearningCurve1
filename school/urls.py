from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
	
    path('school_submit', views.school_submit),
    path('create_event', views.create_event),
    path('event/<str:eventId>',views.event_detail,name="id"),
    path('confirm_volunteers',views.confirm_volunteers),
    path('',views.index)


]