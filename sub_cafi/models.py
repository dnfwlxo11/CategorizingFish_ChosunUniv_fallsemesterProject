from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your models here.

class OverWriteImg(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class ImageUpload(models.Model):
    title = models.CharField(max_length = 255)
    pic = models.FileField(null = True, blank = True, upload_to='', storage=OverWriteImg())

    def __str__(self):
        return self.title