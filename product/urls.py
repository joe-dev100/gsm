
from django.urls import path

from product.views import *

app_name = 'product'
urlpatterns = [
    path('list/', product_view, name='product_view'),
    path('add/', add_product, name='add_product'),
    path('add_new_category/', add_new_category, name='add_new_category'),
    path('add_new_unity/', add_new_unity, name='add_new_unity'),
    path('edit/<int:pk>/',product_update_view,name="product_update_view"),
    

    path('delete/<int:pk>/',product_delete_view,name="product_delete_view"),
  
    path('active/all/',product_active_all_view,name="product_active_all_view"),
    path('deactive/all/',product_deactive_all_view,name="product_deactive_all_view"),
    path('delete/all/',product_delete_all_view,name="product_delete_all_view"),
    path('desactivate/selected/',product_deactivate_selection,name="product_deactivate_selection"),
    path('activate/selected/',product_activate_selection,name="product_activate_selection"),
    path('delete/selected/',product_delete_selection,name="product_delete_selection"),
    # Add other URL patterns here
]