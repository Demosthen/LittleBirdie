from django.shortcuts import render
from .models import file_upload
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


# Create your views here.
class UploadPageView(ListView):
    model = file_upload
    template_name = 'upload.html'

def read_file(request):
    p = "/Users/administrator/Documents/GitHub/LittleBirdie/little_birdie/uscsite/media/text/test.txt"
    f = open(p, 'r')
    file_content = f.read()
    f.close()
    template = loader.get_template('upload.html')
    context = {
        'file_content': file_content
    }
    return HttpResponse(template.render(context))
