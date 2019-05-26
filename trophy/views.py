from django.shortcuts import render
from .models import Profile,Projects
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
    
