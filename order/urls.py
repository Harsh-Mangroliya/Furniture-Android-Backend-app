from django.urls import path
from .views import *

urlpatterns = [
    path('',order.as_view()),
    path('<int:id>/',order.as_view()),
    path('all/<int:userid>/',AllOrder.as_view()),
]