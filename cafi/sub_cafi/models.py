from django.db import models

# Create your models here.

class ImageUpload(models.Model):
    title = models.CharField(max_length = 255)
    pic = models.FileField(null = True, blank = True, upload_to = "")

    def __str__(self):
        return self.title