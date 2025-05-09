from django.urls import path

from stock.views import *

app_name = 'stock'
urlpatterns = [
    path('entree/list/', entree_view, name='entree_view'),
    path('entree/add/', add_entree, name='add_entree'),
    path('entree/add/form/', add_items_form, name='add_items_form'),
    path('entree/filter/', filter_entree_by_date, name='filter_entree_by_date'),
    path('entree/detail/<int:pk>/', entree_details, name='entree_details'),
    path('entree/update/<int:pk>/', entree_update_view, name='entree_update_view'),
    path('entree/delete/item/<int:pk>/', entree_delete_item, name='entree_delete_item'),
    path('entree/update/item/<int:pk>/', entree_update_item, name='entree_update_item'),
    
    path('sortie/list/', sortie_view, name='sortie_view'),
    path('sortie/add/', add_sortie, name='add_sortie'),
    path('sortie/add/form/', add_sortie_items_form, name='add_sortie_items_form'),
    path('sortie/filter/', filter_sortie_by_date, name='filter_sortie_by_date'),
    path('sortie/detail/<int:pk>/', sortie_details, name='sortie_details'),
    path('sortie/update/<int:pk>/', sortie_update_view, name='sortie_update_view'),
    path('sortie/delete/item/<int:pk>/', sortie_delete_item, name='sortie_delete_item'),
    path('sortie/update/item/<int:pk>/', sortie_update_item, name='sortie_update_item'),
]