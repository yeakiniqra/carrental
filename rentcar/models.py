from django.db import models
from django.contrib.auth.models import User

 # Fields for owner sign up
class Owner(models.Model): 
    username = models.CharField(max_length=150, unique=True)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  

    def __str__(self):
        return self.username