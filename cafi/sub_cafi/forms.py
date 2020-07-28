from django import forms
from .models import ImageUpload

class UploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = {'title', 'pic'}