from oauth2client.client import OAuth2WebServerFlow
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from school.models import School
from django.shortcuts import render, redirect
from oauth2client.file import Storage
# Create your views here.


def index(request):
	fileName = request.user.username
	storage = Storage(fileName)
	credentials = storage.get()
	print(credentials)
	return HttpResponse("Done")

def school_submit(request):
	print(request)
	school = request.POST.get("schoolname")
	principal = request.POST.get("principal")
	password = request.POST.get("password")
	email = request.POST.get("email")
	try:
		user = User.objects.create_user(username=principal,password=password,email=email,is_staff=True)
		user.save()
		print("User created")
	except:
	 	return render(request,'login/templates/school.html',{'message':'Username already taken'})

	schoolObj = School.objects.create(principal=user,schoolName=school)
	schoolObj.save()

	return redirect("/authenticate/login")

