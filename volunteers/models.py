from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Volunteer(models.Model):
	volunteer = models.ForeignKey(User,on_delete=models.CASCADE)
	#branch = models.CharField(max_length = 3,choices= (('SC','SC'),('SS','SS'),('MA','MA'),('EN','EN'),('KA','KA'),('EC','EC'),('HI','HI'),('SG','SG'),('SP','SP')))
	field = models.CharField(max_length=20,default="")