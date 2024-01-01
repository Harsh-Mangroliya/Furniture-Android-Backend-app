from django.urls import path
from .views import *

urlpatterns = [
    path('placeorder/',order.as_view()),
    path('allorder/<int:id>/',order.as_view()),
    path('all/<int:userid>/',AllOrder.as_view()),
]
