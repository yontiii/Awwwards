from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    profile_photo = models.ImageField(default='default.jpg',upload_to='profiles/')
    bio = models.TextField(max_length=500,default='Tell Me Something')
    website = models.CharField(max_length=10, blank=True,default='me.com') 
    phone_number = models.CharField(max_length=10,default=12345678)
    
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
     
    @receiver(post_save, sender=User) 
    def save_profile(sender,instance,**kwargs):
        instance.profile.save()  
        
    
    
    def __str__(self):
        return self.bio
    
    
class Projects(models.Model):
    profile = models.ForeignKey(User,on_delete=models.CASCADE) 
    title = models.CharField(max_length=20,blank=True)
    image_landing = models.ImageField(upload_to='landing/')
    description = models.TextField(max_length=200,blank=True)
    link = models.CharField(max_length=20)
    
    
    @classmethod
    def search_by_projects(cls,search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects 
    
    
    @classmethod
    def get_by_id(cls,id):
        project = Projects.objects.get(user = id)
        return profile
    
    @classmethod
    def filter_by_id(cls,id):
        projects = Projects.objects.filter(user = id).first()
        return projects
    
    

    
    



