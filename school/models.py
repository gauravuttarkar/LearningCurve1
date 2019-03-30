from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
	principal = models.ForeignKey(User,on_delete=models.CASCADE)
	schoolName = models.CharField(max_length=100, null=False,default="")

class Volunteer(models.Model):
	username = models.ForeignKey(User,on_delete=models.CASCADE)
	fname = models.CharField(max_length=100,null=False, default = "")
	lname = models.CharField(max_length=100,null=False, default = "")
	email = models.EmailField(max_length=100,null=False, default = "")