from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from config import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('settings/', include('settings.urls')),
    path('category/', include('category.urls')),
    path('unity/', include('unity.urls')),
    path('product/', include('product.urls')),
    path('stock/', include('stock.urls')),
    path('vente/', include('vente.urls')),
    path('facture/', include('facture.urls')),
    path('cash/', include('cash.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()