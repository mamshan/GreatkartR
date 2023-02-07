from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<str:brand>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<str:brand>/<slug:product_slug>/', views.product_detail, name='product_detail'),  
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),   
    path('search/', views.search, name='search'),
    path('search_size/', views.search, name='search_size'),
    path('get_sizes/', views.get_sizes, name='get_sizes'),
    path('upload_image/', views.upload_image),
]



