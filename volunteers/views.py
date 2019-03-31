from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from volunteers.models import Volunteer
from django.shortcuts import render, redirect
from school.models import Prospective, Request, School
# Create your views here.
import requests

def calculateDistace(d1,d2):
	url='https://maps.googleapis.com/maps/api/distancematrix/json'
	payload={
	'origins':'Boston,MA',
	'destinations':'Lexington,MA',
	'key':'AIzaSyCSvYPh9cC2oAzADo7taRjSziWqo8gj258',
	'departure_time':'now'
	}
	r = requests.get(url, params=payload)
	results = r.json()
	print(results)

def index(request):
	yourEvents = Request.objects.all().filter(allocated=request.user.username)

	yourList = []
	for req in yourEvents:
		reqDict = {}
		reqDict['school'] = req.school.schoolName
		reqDict['id'] = req.id
		reqDict['startTime'] = req.startTime
		reqDict['endTime'] = req.endTime

		yourList.append(reqDict)

	print(yourList)
	requestObj = Request.objects.all().filter(allocated=None)
	print(request.user.username)
	requestList = []
	for req in requestObj:
		li = Prospective.objects.all().filter(username=request.user.username,request=req)
		print(li)
		if(len(li)>0):
			requestList.append(req)

	finalReqList = []
	for req in requestList:
		reqDict = {}
		reqDict['school'] = req.school.schoolName
		reqDict['id'] = req.id
		reqDict['startTime'] = req.startTime
		reqDict['endTime'] = req.endTime
		finalReqList.append(reqDict)

	print(finalReqList)
	return render(request,"volunteers/templates/index.html",{'user':request.user,
															'requestList': finalReqList,
															'yourList':yourList})

def confirm_events(request):
	selectReq = request.POST.getlist("selectedEvent")
	print(selectReq)
	selectedDates = [] 
	for event in selectReq:
		requestObj = Request.objects.get(id=event)
		startDate = requestObj.startTime[:10]
		if startDate not in selectedDates:
			requestObj.allocated = request.user.username
			requestObj.save()
			selectedDates.append(startDate)
		else:
			continue	

	return HttpResponse("Done")
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