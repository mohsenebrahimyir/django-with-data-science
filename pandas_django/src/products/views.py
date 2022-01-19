from django.shortcuts import render
from .models import Product, Purchese
import pandas as pd


def chart_select_view(request):
    error_message = None
    df = None

    purchese_df = pd.DataFrame(Purchese.objects.all().values())

    if purchese_df.size > 0:
        product_df = Product.objects.all().values()
        product_df = pd.DataFrame(product_df).drop(['date'], axis=1)
        product_df = product_df.rename(columns=lambda x: "product_"+x)
        df = pd.merge(purchese_df, product_df, on="product_id")
        if request.method == "POST":
            chart_type = request.POST.get('sales')
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']
            print(df['date'])
            df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            print(df['date'])
            df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
            print(df2)

    else:
        error_message = "No records in database"

    context = {
        "error_message": error_message,
    }

    return render(request, "products/main.html", context)
