from django.urls import path
from .views import *

app_name = 'vente'
urlpatterns = [
    path('session/list/', session_list, name='session_list'),  
    path('cart/discount/', discount, name='discount'),  
    path('session/update/<int:pk>/', session_update, name='session_update'),  
    path('cart/add/<int:pk>/', addToCart, name='add_to_cart'),  
    path('cart/incrise/<int:pk>/', increseQty, name='increseQty'),  
    path('cart/decrese/<int:pk>/', decreseQty, name='decreseQty'),  
    path('cart/save/', saveCart, name='saveCart'),  
    path('cart/clear/', clearCart, name='clearAll'),  
    path('cart/pos/', facture, name='pos'),  
]
