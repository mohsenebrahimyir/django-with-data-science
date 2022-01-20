from django.shortcuts import render
from .models import *
import pandas as pd
from .utils import *
from .forms import *
import matplotlib.pyplot as plt
import seaborn as sns

def sales_dist_view(request):
    df = pd.DataFrame(Purchase.objects.all().values())
    df['salesman_id'] = df['salesman_id'].apply(get_salesman_from_id)
    df.rename({'salesman_id': 'salesman'}, axis=1, inplace=True)
    df['date'] = df['date'].apply(lambda x: x.strftime("%Y-%m-%d"))
    
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    sns.barplot(x='date', y='total_price', hue='salesman', data=df)
    plt.tight_layout()
    graph = get_image()
    
    context = {
        'graph': graph,
    }
    
    return render(request, 'products/sales.html', context)

def chart_select_view(request):
    error_message = None
    df = None
    graph = None
    price = None

    purchase_df = pd.DataFrame(Purchase.objects.all().values())

    if purchase_df.size > 0:
        product_df = Product.objects.all().values()
        product_df = pd.DataFrame(product_df).drop(['date'], axis=1)
        product_df = product_df.rename(columns=lambda x: "product_"+x)
        df = pd.merge(purchase_df, product_df, on="product_id")
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


def add_purchase_view(request):
    form = PurchaseForm(request.POST or None)
    added_message=None
    
    if form.is_valid():
        obj = form.save(commit=False)
        obj.salesman = request.user
        obj.save()
        
        form = PurchaseForm()
        added_message="The purchase has been added"
    
    context = {
        'form': form,
        'added_message': added_message,
    }
    return render(request, 'products/add.html', context)