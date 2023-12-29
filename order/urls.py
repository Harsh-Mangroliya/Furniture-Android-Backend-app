from django.urls import path
from .views import *

urlpatterns = [
    path('order/',order.as_view()),
    path('order/<int:id>/',order.as_view()),
    path('all/<int:userid>/',AllOrder.as_view()),
]