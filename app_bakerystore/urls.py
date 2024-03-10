from django.urls import path
from app_bakerystore.views import home_view, contact, ProductListView, product_detail, upload_product, add_to_cart, delete_product, shopping_cart, finalizeaza_comanda


# in this file we define our Bakery_store application specific routes
app_name = 'app_bakerystore'  # in the app_name variable we save the name of the application where we defined our application specific urls
                                      # we will use this name when we manage the urls in the templates (html files)

urlpatterns = [
    path('', home_view, name='home'),
    path('upload_product/', upload_product, name='upload-product'),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:product_id>/', product_detail, name='product'),
    path('shopping_cart/', shopping_cart, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('finalizeaza_comanda/', finalizeaza_comanda, name='order_complete'),
    path('contact/', contact, name='contact'),
    ]
