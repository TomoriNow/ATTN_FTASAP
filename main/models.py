from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
import uuid

GENDER_CHOICES = [("Male", "Male"),("Female", "Female")]
class AccountUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userID = models.UUIDField(default=uuid.uuid4)
    firstName = models.CharField(max_length= 20)
    lastName = models.CharField(max_length= 20)
    gender = models.CharField(max_length= 10, choices = GENDER_CHOICES)
    birthDate = models.DateField()
    address = models.TextField()
    is_staff = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)

class Staff(models.Model):
    user = models.OneToOneField(AccountUser, on_delete=models.CASCADE)
    NIK = models.CharField(max_length=50)
    NPWP = models.CharField(max_length=50)
    BankAccount = models.CharField(max_length=50)
    BankName = models.CharField(max_length=50)

class Child(models.Model):
    user = models.OneToOneField(AccountUser, on_delete=models.CASCADE)
    dadName = models.CharField(max_length=50)
    momName = models.CharField(max_length=50)
    dadJob = models.CharField(max_length=20)
    momJob = models.CharField(max_length=20)
    