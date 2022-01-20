from django.shortcuts import render
from .forms import CsvForm


def upload_file_view(request):
    return render(request, 'csvs/upload.html', {})
