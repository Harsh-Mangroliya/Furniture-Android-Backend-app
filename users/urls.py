from django.urls import path
from .views import *


urlpatterns = [
    
    path('login/',LoginView.as_view()),
    path('crud/',UserView.as_view()),
    path('crud/<int:id>/',UserView.as_view()),
    path('card/',CardDetailView.as_view()),
    path('card/<int:id>/',CardDetailView.as_view()),

    path('verifyotp/',OTPVerifyView.as_view()),

]
