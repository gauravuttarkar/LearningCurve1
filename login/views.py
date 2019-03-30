from oauth2client.client import OAuth2WebServerFlow
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from . import templates
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
import httplib2
from googleapiclient.discovery import build
import datetime
import pickle
# Create your views here.
def login(request):
	print("Hitting Home Page Successfull")

	#return HttpResponse("Done and dusted")
	return render(request,'login/templates/login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')


def signup(request):
	return render(request,'login/templates/signup.html')

def signup_select(request):
    choice = request.POST.get('optradio')
    print(choice)
    if choice == "school":
        return render(request,'login/templates/school.html')
    else:
        return render(request,'login/templates/volunteer.html')

def signup_submit(request):
    print("Creating a new user")
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    user = User.objects.create_user(username, email,password)
    user.save()
    return redirect('/authenticate/login')



def logging_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        auth.login(request,user)
        return redirect('/')
        # Redirect to a success page.
        ...
    else:
        return redirect('/authenticate/login')
        # Return an 'invalid login' error message.


def signup_vol(request):
    username = request.POST['username']
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    confpass = request.POST['confpass']
    


def google(request):
    flow = OAuth2WebServerFlow(client_id='57992333576-0se8v3dt80u59hebq7v62fcchgh69e78.apps.googleusercontent.com',
                           client_secret='BEzkUE-qn0mMWK7HB_lFSfBM',
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='https://59c83093.ngrok.io/authenticate/redirect')
    auth_uri = flow.step1_get_authorize_url()
    print(auth_uri)
    print("redirecting")
    return HttpResponseRedirect(auth_uri)

def redirect(request):
    flow = OAuth2WebServerFlow(client_id='57992333576-0se8v3dt80u59hebq7v62fcchgh69e78.apps.googleusercontent.com',
                           client_secret='BEzkUE-qn0mMWK7HB_lFSfBM',
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='https://59c83093.ngrok.io/authenticate/redirect')
    code = request.GET.get("code")
    credentials = flow.step2_exchange(code)
    http = httplib2.Http()
    http = credentials.authorize(http)
    print(credentials)
    service = build('calendar', 'v3', http=http)
    print(service)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return HttpResponseRedirect("/calendar")

