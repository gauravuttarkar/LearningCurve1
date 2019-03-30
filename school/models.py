from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
	principal = models.ForeignKey(User,on_delete=models.CASCADE)
	schoolName = models.CharField(max_length=100, null=False,default="")
	credentials = models.CharField(max_length=100)
	location = models.CharField(max_length=100, null = False, default = "12.3052032,76.6222336")
