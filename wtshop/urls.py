
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shops import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view() , name='login'),
    path('api/signup/', views.SignUpAPIView.as_view(), name='api-register'),
    path('api/products/', views.ProductListView.as_view(), name='api-products'),
    path('api/orders/', views.OrderItems.as_view(), name='order-items'),
     path('api/address/', views.AddressCreateAPIView.as_view(), name="api-address"),
    # path('api/products/<int:product_id>/', views.ProductDetails.as_view(), name='api-product-detail'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
