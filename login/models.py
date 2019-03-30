from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class RedirectState(models.Model):
    # """Model to store YA oauth requests with users
    #
    # Create a new entry between the user and the oauth state
    #
    # Fields:
    #     user (User): Your application user
    #     state (str): A unique ID which helps in matching an oauth2 code from YA to a user
    # """
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.IntegerField()
    state = models.CharField(max_length=512, null=False)