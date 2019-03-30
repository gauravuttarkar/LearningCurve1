
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from school.models import School
from django.shortcuts import render, redirect
# Create your views here.

def school_submit(request):
	print(request)
	school = request.POST.get("schoolname")
	principal = request.POST.get("principal")
	password = request.POST.get("password")
	user = User.objects.create_user(username=principal,password=password)
	user.save()

	schoolObj = School.objects.create(principal=user,schoolName=school)
	schoolObj.save()

	return redirect("/")