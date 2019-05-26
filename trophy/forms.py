from django import forms
from .models import Profile,Projects


class ProjectUploadForm(forms.ModelForm):
    class Meta:
        fields = ('title','image_landing','description', 'link')