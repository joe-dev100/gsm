from django.urls import path
from .views import *

app_name = 'vente'
urlpatterns = [
    path('session/list/', session_list, name='session_list'),  
    path('cart/discount/', discount, name='discount'),  
    path('session/open/<int:pk>/', open_session, name='open_session'),  
    path('session/close/<int:pk>/', close_session, name='close_session'),  
    path('cart/add/<int:pk>/', addToCart, name='add_to_cart'),  
    path('cart/incrise/<int:pk>/', increseQty, name='increseQty'),  
    path('cart/changeQty/<int:pk>/', change_qty_in_input, name='change_qty_in_input'),  
    path('cart/decrese/<int:pk>/', decreseQty, name='decreseQty'),  
    path('cart/delete/<int:pk>/', deleteItemInCart, name='deleteItemInCart'),  
    path('cart/save/', saveCart, name='saveCart'),  
    path('cart/clear/', clearCart, name='clearAll'),  
    path('cart/pos/', facture, name='pos'),  
    path('cart/cancel/', cancelPrint, name='cancelPrint'),  
]
