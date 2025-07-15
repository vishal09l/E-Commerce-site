from django.contrib import admin
from django.urls import path
from store.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove_one_from_cart/<int:product_id>/', remove_one_from_cart, name='remove_one_from_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product_list/', product_list, name='product_list'),
    path('login/', login_page, name='login'),
    path('adminlogin/', admin_login, name='admin_login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register, name='register'),
    path('men/', men_products, name='men_products'),
    path('women/', women_products, name='women_products'),
    path('kids/', kids_products, name='kids_products'),
    path('fashion/', fashion_products, name='fashion_products'),
    path('dashboard/', dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
