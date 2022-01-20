from django.urls import path
from .views import *

app_name = "customers"

urlpatterns = [
    path('', customer_corr_view, name='main-customers-view'),
]