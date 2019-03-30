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
from oauth2client.file import Storage
from school.models import School
import uuid
from login.models import RedirectState
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
        print("Successfull")
        return HttpResponseRedirect('/authenticate/google')
        # Redirect to a success page.
        ...
    else:
        print("Fail")
        return redirect('/authenticate/login')
        # Return an 'invalid login' error message.
        ...	

def google(request):
    state = str(uuid.uuid4())
    flow = OAuth2WebServerFlow(client_id='57992333576-0se8v3dt80u59hebq7v62fcchgh69e78.apps.googleusercontent.com',
                           client_secret='BEzkUE-qn0mMWK7HB_lFSfBM',
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='https://f97d0c04.ngrok.io/authenticate/redirect',
                           state=state)
    auth_uri = flow.step1_get_authorize_url()
    user = User.objects.get(id=request.user.id)
    RedirectState.objects.create(user=user.id, state=state)
    print(state)
    print(auth_uri)
    print("redirecting")
    return HttpResponseRedirect(auth_uri)

def redirect(request):
    flow = OAuth2WebServerFlow(client_id='57992333576-0se8v3dt80u59hebq7v62fcchgh69e78.apps.googleusercontent.com',
                           client_secret='BEzkUE-qn0mMWK7HB_lFSfBM',
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='https://f97d0c04.ngrok.io/authenticate/redirect')
    code = request.GET.get("code")
    state = request.GET.get("state")
    redirect_state = RedirectState.objects.get(state=state)
    user = redirect_state.user
    print(state)
    
    user = User.objects.get(id=user)
    print("User",user)
    fileName = user.username
    # user = User.objects.get(username=fileName)
    #print(request.user.is_staff)
    #print("Filename is",fileName)
    print("File",fileName)
    print("is staff",user.is_staff)
    credentials = flow.step2_exchange(code)
    http = httplib2.Http()
    http = credentials.authorize(http)
    print(credentials)
    
    #storing in the credentials
    storage = Storage(fileName)
    storage.put(credentials)


    return HttpResponseRedirect("/school")

def signup_vol(request):
    username = request.POST['username']
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    confpass = request.POST['confpass']