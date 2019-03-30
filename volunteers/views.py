from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from volunteers.models import Volunteer
from django.shortcuts import render, redirect
# Create your views here.

def index(request):
	return render(request,"volunteers/templates/index.html")

def vol_submit(request):
	print("Volunteers entered to db")
	username = request.POST['username']
	fname = request.POST['fname']
	lname = request.POST['lname']
	email = request.POST['email']
	field = request.POST['field']
	loc = request.POST['loc']
	password = request.POST['password']
	confpass = request.POST['confpass']

	try:
		user = User.objects.create_user(username=username,password=password,email=email,is_staff=False)
		user.save()
		print("User created")
	except:
	 	return render(request,'login/templates/school.html',{'message':'Username already taken'})

	schoolObj = Volunteer.objects.create(volunteer=user,field=field, location = loc)
	schoolObj.save()

	return redirect("/authenticate/login")