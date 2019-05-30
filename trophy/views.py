from django.shortcuts import render,redirect
from django.http import Http404
from .models import Profile,Projects,Rates,Comments
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from .serializer import ProfileSerializer,ProjectsSerializer
from .forms import ProfileEditForm,ProjectUploadForm,VotesForm,ReviewForm
# Create your views here.
def home(request):
    projects = Projects.objects.all()
    
    context = {
        'projects':projects,
    }
    return render(request,'home.html',context)


def projects(request,project_id):
    try:
        projects = Projects.objects.get(id=project_id)
        all = Rates.objects.filter(project=project_id) 
        print(all)
    except Exception as e:
        raise Http404() 
    
    # single user votes count
    count = 0
    for i in all:
        count+=i.usability
        count+=i.design
        count+=i.content
    
    if count > 0:
        average = round(count/3,1)
    else:
        average = 0
        
    if request.method == 'POST':
        form = VotesForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project_id
            rate.save()
        return redirect('projects',project_id)
        
    else:
        form = VotesForm() 
        
    # The votes logic
    votes = Rates.objects.filter(project=project_id)
    usability = []
    design = []
    content = [] 
    
    for i in votes:
        usability.append(i.usability)
        design.append(i.design)
        content.append(i.content) 
        
    if len(usability) > 0 or len(design)>0 or len(content)>0:
        average_usability = round(sum(usability)/len(usability),1) 
        average_design = round(sum(design)/len(design),1)
        average_content = round(sum(content)/len(content),1) 
            
        average_rating = round((average_content+average_design+average_usability)/3,1) 
    
    else:
        average_content=0.0
        average_design=0.0
        average_usability=0.0
        average_rating = 0.0
        
    '''
    To make sure that a user only votes once
    '''
    
    arr1 = []
    for use in votes:
        arr1.append(use.user_id) 
                
    auth = arr1
       
    reviews = ReviewForm(request.POST)
    if request.method == 'POST':
        
        if reviews.is_valid():
            comment = reviews.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect ('projects',project_id)
        else:
            reviews = ReviewForm()
            
        
    user_comments = Comments.objects.filter(pro_id=project_id)
       
    context = {
        'projects':projects,
        'form':form,
        'usability':average_usability,
        'design':average_design,
        'content':average_content,
        'average_rating':average_rating,
        'auth':auth,
        'all':all,
        'average':average,
        'comments':user_comments,
        'reviews':reviews,
        
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


@login_required(login_url='/accounts/login/')
def post_site(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            home = form.save(commit=False)
            home.profile =current_user
            form.save()
        return redirect('home')
    else:
        form =ProjectUploadForm()
            
    return render(request,'uploads.html',{"form":form,})


class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProjectsList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        all_projects = Projects.objects.all()
        serializers = ProjectsSerializer(all_projects,many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = ProjectsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    



def search_results(request):
    if 'titles' in request.GET and request.GET['titles']:
        search_term = request.GET.get("titles")
        searched_projects = Projects.search_by_projects(search_term)
        
        message = f'{search_term}'
        
        return render(request,'search.html',{"message":message,"projects":searched_projects})
    
    else:
        message = "You haven't searched for any term"
        return render(request,'search.html',{"message":message,"projects":searched_projects})