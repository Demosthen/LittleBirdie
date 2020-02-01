from django.urls import path
from .views import UploadPageView
from .views import read_file

app_name = "file"

urlpatterns = [
    path('read/', read_file, name='read'),
]
