from django.db import models
from django.contrib.auth.models import User

class AccountUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userID = models.UUIDField()
    firstName = models.CharField(max_length= 20)
    lastName = models.CharField(max_length= 20)
    gender = models.CharField(max_length= 10)
    birthDate = models.DateField()
    address = models.TextField()
    