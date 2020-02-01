from django.db import models
from django.conf import settings

class file_upload(models.Model):
    #id = 0
    text = models.FileField(upload_to='text/')
    #def __init__(self):
        #self.id = id
        #file_upload.id+=1
    #cover = models.ImageField(upload_to='text/')


# Create your models here.
