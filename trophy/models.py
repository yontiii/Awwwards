from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Projects(models.Model):
    title = models.CharField(max_length=20,blank=True)
    image_landing = models.ImageField(upload_to='landing/')
    description = models.TextField(max_length=200,blank=True)
    link = models.CharField(max_length=20)
    
    



