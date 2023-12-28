from django.urls import path
from .views import *


urlpatterns = [
    
    path('login/',LoginView.as_view()),
    path('crud/',UserView.as_view()),
    path('crud/<int:id>/',UserView.as_view()),
    path('sendmail/',sendMain)
]
