from itertools import product
from multiprocessing import context
from turtle import pd
from django.shortcuts import render
from .models import Product, Purchese
import pandas as pd


def chart_select_view(request):
    products_df = pd.DataFrame(Product.objects.all().values())
    purchese_df = pd.DataFrame(Purchese.objects.all().values())
    
    context = {
        "products": products_df.to_html(),
        "purchese": purchese_df.to_html(),
    }
    return render(request, "products/main.html", context)