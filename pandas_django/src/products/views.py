from django.shortcuts import render
from .models import Product, Purchese
import pandas as pd


def chart_select_view(request):
    product_df = pd.DataFrame(Product.objects.all().values())
    purchese_df = pd.DataFrame(Purchese.objects.all().values())
    col_rename = {col:"product_" + col for col in product_df.columns}
    product_df = product_df.rename(col_rename, axis=1)
    df = pd.merge(product_df, purchese_df, on="product_id")
    context = {
        "products": product_df.to_html(),
        "purchese": purchese_df.to_html(),
        "dataframe": df.to_html(),
    }
    return render(request, "products/main.html", context)