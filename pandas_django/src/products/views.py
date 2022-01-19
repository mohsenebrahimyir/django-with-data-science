from django.shortcuts import render
from .models import Product, Purchese
import pandas as pd


def chart_select_view(request):
    error_message = None
    product_df = pd.DataFrame(Product.objects.all().values())
    rename_col = {col:"product_" + col for col in product_df.columns}
    product_df = product_df.rename(rename_col, axis=1)
    purchese_df = pd.DataFrame(Purchese.objects.all().values())
    
    if purchese_df.size > 0:
        df = pd.merge(purchese_df, product_df, on="product_id").drop(['product_date'], axis=1)
        if request.method == "POST":
            chart_type = request.POST.get('sales')
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']
    else:
        error_message = "No records in database"
        df = None
    
    context = {
        "error_message": error_message,
    }
    
    return render(request, "products/main.html", context)