from django.urls import path
from .views import *

urlpatterns = [
    path('placeorder/',order.as_view(),name='place_order'),
    path('order/<int:id>/',order.as_view(),name='order_detail'),
    path('all/<int:id>/',AllOrder.as_view(),name='all_orders'),
]
