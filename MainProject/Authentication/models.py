from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    #custom user profile with a one to one relationship with the default user model
    #now the database can contain a team associated with each user
    team_name = models.CharField(max_length=100, blank=True, null=True)