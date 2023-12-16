from django.urls import path
from .views import table_view
from main.views import index

urlpatterns = [
    path('',  index),
    path('table/', table_view, name='table-view'),
]