from django.urls import path
from . import views
from .login_views import  login


urlpatterns = [
    path('', views.bot_start, name='bot_start'),
    # path('', Home.as_view(), name='home'),
    path('test/', views.test, name='test'),
    path('greet/', views.greet, name='greet'),
    path('chatbot/', views.chatbot, name='chatbot'),


    path('api/login', login),
]
