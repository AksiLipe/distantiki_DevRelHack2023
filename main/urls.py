from django.urls import path

from main.views import index, table_view

urlpatterns = [
    path('table/', table_view),
    path('',  index),
]