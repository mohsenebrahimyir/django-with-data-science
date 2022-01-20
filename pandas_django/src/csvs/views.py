from django.shortcuts import render
from .forms import CsvForm
from .models import *
import pandas as pd
from django.contrib.auth.models import User
from products.models import Product, Purchase
from django.contrib.auth.decorators import login_required


@login_required
def upload_file_view(request):
    error_message = None
    success_message = None
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm()
        try:
            obj = Csv.objects.get(activated = False)
            reader = pd.read_csv(obj.file_name.path, ";", header=None)
            reader = reader.drop(reader.columns[5], axis=1)
            for row in reader.iloc:
                user = User.objects.get(id=row[3])
                prod, _ = Product.objects.get_or_create(name=row[0])
                Purchase.objects.create(
                    product = prod,
                    price = int(row[2]),
                    quantity = int(row[1]),
                    salesman = user,
                    date = row[4]
                )
            obj.activated = True
            obj.save()
            success_message = "Uploaded successfully"
        except:
            error_message = "Ups. Something were wrong..."

    context = {
        'form': form,
        "error_message": error_message,
        "success_message": success_message,
    }
    return render(request, 'csvs/upload.html', context)
