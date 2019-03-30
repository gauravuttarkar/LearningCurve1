from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from volunteers.models import Volunteer
from django.shortcuts import render, redirect
# Create your views here.

def vol_submit(request):
	username = request.POST['username']
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    confpass = request.POST['confpass']

	try:
		user = User.objects.create_user(username=username,password=password,email=email,is_staff=True)
		user.save()
		print("User created")
	except:
	 	return render(request,'login/templates/school.html',{'message':'Username already taken'})

	schoolObj = School.objects.create(principal=user,schoolName=school)
	schoolObj.save()

	return redirect("/authenticate/login")