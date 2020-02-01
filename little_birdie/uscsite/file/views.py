from django.shortcuts import render
from .models import file_upload
from django.views.generic import ListView, CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import os
from .post_file import PostForm # new
from django.urls import reverse_lazy # new



# Create your views here.
class UploadPageView(ListView):
    model = file_upload
    template_name = 'upload.html'

class CreatePostView(CreateView): # new
    model = file_upload
    form_class = PostForm
    template_name = 'post_file.html'
    success_url = '/read/'

#def add_file(request):


def read_file(request):
    #p = "/Users/administrator/Documents/GitHub/LittleBirdie/little_birdie/uscsite/media/text/test.txt"
    folder = "media/text"
    file_content = "hello"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            f = open(file_path, 'r')
            file_content = f.read()
            f.close()
        except:
            print('uh oh')
    #"../media/text/test.txt"
    template = loader.get_template('upload.html')
    str = "does this work"
    context = {
        'file_content': file_content,
        'test': str
    }
    return HttpResponse(template.render(context))
