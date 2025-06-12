from .views import *
from django.urls import path
app_name = 'cash'
urlpatterns = [
    path('confirmation/', cash_confirmation, name='cash_confirmation'),
    path('entree/', entree_cash, name='entree_cash'),
    path('sortie/', sortie_cash, name='sortie_cash'),
    path('change/', change_devise, name='change_devise'),
    path('entree/<int:pk>/', delete_entree, name='delete_entree'),
    path('sortie/<int:pk>/', delete_sortie, name='delete_sortie'),
    
]