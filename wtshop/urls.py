
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shops import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', views.ProductListView.as_view(), name='api-products'),
    # path('api/products/<int:product_id>/', views.ProductDetails.as_view(), name='api-product-detail'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
