from django.shortcuts import render
from .models import Profile,Projects
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    projects = Projects.objects.all()
    
    context = {
        'projects':projects,
    }
    return render(request,'home.html',context)


def projects(request,project_id):
    projects = Projects.objects.get(id=project_id)
    
    context = {
        'projects':projects,
    }
    
    return render(request,'single_post.html',context) 



@login_required(login_url='/accounts/login/')
def profile(request,username):
    profile = User.objects.get(username=username)
    
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    projects = Projects.get_profile_projects(profile.id)
    
    return render(request, 'users/profile.html',{"profile":profile,"profile_details":profile_details,"projects":projects}) 
    
