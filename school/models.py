from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
	principal = models.ForeignKey(User,on_delete=models.CASCADE)
	schoolName = models.CharField(max_length=100, null=False,default="")
<<<<<<< HEAD

class Volunteer(models.Model):
	username = models.ForeignKey(User,on_delete=models.CASCADE)
	fname = models.CharField(max_length=100,null=False, default = "")
	lname = models.CharField(max_length=100,null=False, default = "")
	email = models.EmailField(max_length=100,null=False, default = "")
=======
	credentials = models.CharField(max_length=100)
>>>>>>> 6cb73b1fa7fb97bd3f7034f95bc006e5797f44ab
