from distutils.command.upload import upload
from django.urls import path
from .views import *

app_name = "csvs"

urlpatterns = [
    path('', upload_file_view, name='upload-view'),
]
