from django.contrib import admin
from django.urls import path
from store.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('product_list/', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('login/', login_page, name='login_page'),
    path('register/', register, name='register'),
    path('logout/', logout_page, name='logout'),  
    path('women/', women_products, name='women_products'),
    path('men/', men_products, name='men_products'),
    path('kids/', kids_products, name='kids_products'),
    path('fashion/', fashion_products, name='fashion_products'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
