from django.urls import path
from .views import *



urlpatterns = [
    path('list/', ProductView.as_view(), name='product'),
    path('list/<int:id>/', ProductView.as_view(), name='product'),
    path('addtocart/',cartView.as_view()),
    path('addtocart/<int:id>/',cartView.as_view()),
]