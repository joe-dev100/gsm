from .views import *
from django.urls import path
app_name = 'category'
urlpatterns = [
    path('list/',category_view,name="category_list_view"),
    path('edit/<int:pk>/',category_update_view,name="category_update_view"),
    

    path('delete/<int:pk>/',category_delete_view,name="category_delete_view"),
    path('add/',category_add_view,name="category_add_view"),
    path('active/all/',category_active_all_view,name="category_active_all_view"),
    path('deactive/all/',category_deactive_all_view,name="category_deactive_all_view"),
    path('delete/all/',category_delete_all_view,name="category_delete_all_view"),
    path('desactivate/selected/',category_deactivate_selection,name="category_deactivate_selection"),
    path('activate/selected/',categorie_activate_selection,name="categorie_activate_selection"),
    path('delete/selected/',categorie_delete_selection,name="categorie_delete_selection"),
    
]