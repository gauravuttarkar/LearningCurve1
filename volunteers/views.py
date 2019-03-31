from django.shortcuts import render, redirect
from oauth2client.client import OAuth2WebServerFlow
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from volunteers.models import Volunteer
from django.shortcuts import render, redirect
from school.models import Prospective, Request, School
from oauth2client.file import Storage
from googleapiclient.discovery import build
import httplib2
import datetime
# Create your views here.
import requests


def createCalendar(request,summary,location,startTime,endTime):
	fileName = request.user.username
	storage = Storage(fileName)
	credentials = storage.get()
	print(credentials)
	http = httplib2.Http()
	http = credentials.authorize(http)
	print(request.user.username)
	#schoolObj = School.objects.get(principal=request.user)
	#print(schoolObj)
	#print(schoolObj.location)
	#location = schoolObj.location
	#print(location)
	service = build('calendar', 'v3', http=http)
	event = {
		'summary': summary,
		'location': location,
		
		'start': {
		'dateTime': startTime,
		'timeZone': '(GMT+05.30)',
		},
		'end': {
		'dateTime': endTime,
		'timeZone': '(GMT+05.30)',
		},
		'recurrence': [
		'RRULE:FREQ=DAILY;COUNT=1'
		],
		'attendees': [
		{'email': 'lpage@example.com'},
		{'email': 'sbrin@example.com'},
		],
		'reminders': {
		'useDefault': False,
		'overrides': [
		{'method': 'email', 'minutes': 24 * 60},
		{'method': 'popup', 'minutes': 10},
		],
		},
	}
	event = service.events().insert(calendarId='primary', body=event).execute()
	return
def calculateDistace(d1,d2):
	url='https://maps.googleapis.com/maps/api/distancematrix/json'
	payload={
	'origins':d1,
	'destinations':d2,
	'key':'AIzaSyCSvYPh9cC2oAzADo7taRjSziWqo8gj258',
	'departure_time':'now'
	}
	r = requests.get(url, params=payload)
	results = r.json()
	print(results)
	duration = results['rows'][0]['elements'][0]['duration']['text']
	distance = results['rows'][0]['elements'][0]['distance']['text']

	return [distance, duration]

def index(request):
	print('IN index',request.user.username)
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
	volunteerObj = Volunteer.objects.get(volunteer=request.user)
	finalReqList = []
	for req in requestList:
		reqDict = {}
		reqDict['school'] = req.school.schoolName
		reqDict['id'] = req.id
		reqDict['startTime'] = req.startTime
		reqDict['endTime'] = req.endTime
		li = calculateDistace(req.school.location,volunteerObj.location)
		print(li)
		reqDict['distance'] = li[0]
		reqDict['duration'] = li[1]
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
			
			createCalendar(request,requestObj.school.schoolName,requestObj.school.location,requestObj.startTime[:-6],requestObj.endTime[:-6])
			selectedDates.append(startDate)
		else:
			continue	

	return redirect("/volunteers")
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