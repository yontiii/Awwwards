from django.shortcuts import render
from .models import Profile,Projects
# Create your views here.
def home(request):
    projects = Projects.objects.all()
    
    context = {
        'projects':projects,
    }
    return render(request,'home.html',context)
