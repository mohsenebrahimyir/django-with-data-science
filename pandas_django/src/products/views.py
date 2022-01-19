from django.shortcuts import render
from .models import Product, Purchese
import pandas as pd


def chart_select_view(request):
    product_df = pd.DataFrame(Product.objects.all().values())
    rename_product_col = {col:"product_" + col for col in product_df.columns}
    product_df = product_df.rename(rename_product_col, axis=1)
    purchese_df = pd.DataFrame(Purchese.objects.all().values())
    df = pd.merge(purchese_df, product_df, on="product_id").drop(['product_date'], axis=1)
    context = {
        "products": product_df.to_html(),
        "purchese": purchese_df.to_html(),
        "dataframe": df.to_html(),
    }
    return render(request, "products/main.html", context)