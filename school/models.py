from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
	principal = models.ForeignKey(User,on_delete=models.CASCADE)
	schoolName = models.CharField(max_length=100, null=False,default="")
	credentials = models.CharField(max_length=100)
	location = models.CharField(max_length=100, null = False, default = "12.3052032,76.6222336")

class Request(models.Model):
	school = models.ForeignKey(School,on_delete=models.CASCADE)
	startTime = models.CharField(max_length=100)
	endTime = models.CharField(max_length=100)
	allocated = models.CharField(max_length=100,default=None,null=True)
	
class Prospective(models.Model):
	request = models.ForeignKey(Request,on_delete=models.CASCADE)
	username = models.CharField(max_length=100,default="")