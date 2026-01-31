from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)