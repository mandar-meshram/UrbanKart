from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('view/', views.view_cart, name='view_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
]
