from django.shortcuts import render
from .models import Product, Purchese
import pandas as pd
from .utils import get_simple_plot


def chart_select_view(request):
    error_message = None
    df = None
    graph = None
    price = None

    purchese_df = pd.DataFrame(Purchese.objects.all().values())

    if purchese_df.size > 0:
        product_df = Product.objects.all().values()
        product_df = pd.DataFrame(product_df).drop(['date'], axis=1)
        product_df = product_df.rename(columns=lambda x: "product_"+x)
        df = pd.merge(purchese_df, product_df, on="product_id")
        price = df['price']
        if request.method == "POST":
            chart_type = request.POST['sales']
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']

            df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
            
            if chart_type != "":
                if date_from != "" and date_to != "":
                    df = df[(df['date']>date_from) & (df['date']<date_to)]
                    df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
                #TODO: function to get a gragh
                graph = get_simple_plot(chart_type, x=df2['date'], y=df2['total_price'], data=df)
            else:
                error_message = "Please select a chart type to continue"

    else:
        error_message = "No records in database"

    context = {
        'price': price,
        "graph": graph,
        "error_message": error_message,
    }

    return render(request, "products/main.html", context)
