from django import forms
from .models import Profile,Projects,Rates


class ProjectUploadForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ('title','image_landing','description', 'link')
        
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_photo','bio','website') 
        
class VotesForm(forms.ModelForm):
    class Meta:
        model = Rates
        fields = ('design','usability','content')
        