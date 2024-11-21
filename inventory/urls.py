from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('add-worker/', views.add_worker, name='add_worker'),
    path('enter-stock/', views.enter_stock, name='enter_stock'),
    path('create-product/', views.create_product, name='create_product'),
    path('define-sub-parts/', views.define_sub_parts, name='define_sub_parts'),
    path('check-stock/', views.check_stock, name='check_stock'),
    path('add-raw-material/', views.add_raw_material, name='add_raw_material'),
    path('view-raw-materials/', views.view_raw_materials, name='view_raw_materials'),
    path('enter-stock/', views.enter_stock, name='enter_stock'),
]
