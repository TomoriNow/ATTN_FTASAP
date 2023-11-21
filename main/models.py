from django.contrib.auth.models import AbstractUser
from django.db import models

class AccountUser(AbstractUser):
    email = models.EmailField()
    userID = models.UUIDField()
    phoneNumber = models.CharField(max_length=15)
    firstName = models.CharField(max_length= 20)
    lastName = models.CharField(max_length= 20)
    gender = models.CharField(max_length= 10)
    birthDate = models.DateField()
    address = models.TextField()
    
