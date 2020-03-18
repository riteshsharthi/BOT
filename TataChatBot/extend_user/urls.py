from django.urls import path
from . import views


urlpatterns = [
    ################################ entity ###############################
    path('index/', views.index, name='index'),
]
