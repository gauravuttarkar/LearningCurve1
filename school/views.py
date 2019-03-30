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
	    start = event['start'].get('dateTime', event['start'].get('date'))
	    print(start, event['summary'])
	    eventList.append(event['summary'])
	#return HttpResponse("Done")
	return render(request,"school/templates/index.html",{'events':eventList})

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

