
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shops import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view() , name='login'),
    path('signup/', views.SignUpAPIView.as_view(), name='register'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('orders/', views.OrderItems.as_view(), name='order-items'),
    path('address/', views.AddressCreateView.as_view(), name="address"),
    path('profile/', views.ProfileView.as_view(), name="address"),
    path('cart/', views.CartView.as_view(), name="address"),
    path('remove/', views.RemoveItems.as_view(), name="address"),

    # path('products/<int:product_id>/', views.ProductDetails.as_view(), name='product-detail'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
