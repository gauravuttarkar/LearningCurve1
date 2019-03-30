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
from googleapiclient.discovery import build
import httplib2
import datetime
from volunteers.models import Volunteer 
# Create your views here.


def index(request):
	fileName = request.user.username
	storage = Storage(fileName)
	credentials = storage.get()
	print(credentials)
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('calendar', 'v3', http=http)
	print(service)
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print('Getting the upcoming 10 events')
	events_result = service.events().list(calendarId='primary', timeMin=now,
	                                    maxResults=10, singleEvents=True,
	                                    orderBy='startTime').execute()
	events = events_result.get('items', [])
	eventList = []
	if not events:
	    print('No upcoming events found.')
	for event in events:
	    di = {}
	    start = event['start'].get('dateTime', event['start'].get('date'))
	    print(start, event['summary'])
	    di['summary'] = event['summary']
	    di['id'] = event['id']
	   
	    eventList.append(di)
	#return HttpResponse("Done")
	return render(request,"school/templates/index.html",{'events':eventList})

def school_submit(request):
	print(request)
	school = request.POST.get("schoolname")
	principal = request.POST.get("principal")
	password = request.POST.get("password")
	location = request.POST.get("location")
	email = request.POST.get("email")
	location = request.POST['loc']
	try:
		user = User.objects.create_user(username=principal,password=password,email=email,is_staff=True)
		user.save()
		print("User created")
	except:
	 	return render(request,'login/templates/school.html',{'message':'Username already taken'})

	schoolObj = School.objects.create(principal=user,schoolName=school, location = location)
	schoolObj.save()

	return redirect("/authenticate/login")

def create_event(request):
	branch = request.POST.get("branch")
	startTime = request.POST.get("startTime")
	endTime = request.POST.get("endTime")
	startDate = request.POST.get("startDate")
	endDate = request.POST.get("endDate")
	summary = request.POST.get("summary")
	print(startDate,endDate,startTime,endTime)
	fileName = request.user.username
	storage = Storage(fileName)
	credentials = storage.get()
	print(credentials)
	http = httplib2.Http()
	http = credentials.authorize(http)
	schoolObj = School.objects.get(principal=request.user)
	print(schoolObj)
	print(schoolObj.location)
	location = schoolObj.location
	#print(location)
	service = build('calendar', 'v3', http=http)
	event = {
		'summary': summary,
		'location': location,
		'description': branch,
		'start': {
		'dateTime': startDate + 'T' + startTime + ":00",
		'timeZone': '(GMT+05.30)',
		},
		'end': {
		'dateTime': endDate + 'T' + endTime + ":00",
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


	return HttpResponse("Done")

def event_detail(request,eventId):
	print(eventId)
	fileName = request.user.username
	storage = Storage(fileName)
	credentials = storage.get()
	print(credentials)
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('calendar', 'v3', http=http)
	event = service.events().get(calendarId='primary',eventId=eventId).execute()
	#event = service.events().get(id=eventId)
	print(event)
	di = {}
	di['creator'] = event['creator']['displayName']
	di['email'] = event['creator']['email']
	di['description'] = event['description']
	volunteers = User.objects.all().filter(is_staff=False)
	volunteerDict = {}
	listOfVolunteers = []
	for volunteer in volunteers:
		print(volunteer.username)
		volunteerDict['username'] = volunteer.username
		volunteerObj = Volunteer.objects.get(volunteer=volunteer)
		print(volunteerObj.field)
		volunteerDict['field'] = volunteerObj.field
		listOfVolunteers.append(volunteerDict)
	return render(request, "school/templates/eventDetail.html", {'event':di,
																 'volunteers':listOfVolunteers})

