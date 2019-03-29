from oauth2client.client import OAuth2WebServerFlow
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from . import templates
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
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
        ...	

def google(request):
    flow = OAuth2WebServerFlow(client_id='57992333576-0se8v3dt80u59hebq7v62fcchgh69e78.apps.googleusercontent.com',
                           client_secret='BEzkUE-qn0mMWK7HB_lFSfBM',
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='https://56f47de3.ngrok.io/authenticate/redirect')
    auth_uri = flow.step1_get_authorize_url()
    print(auth_uri)

    return redirect(auth_uri)

def redirect(request):
    print(request)
    return HttpResponseRedirect("/")

