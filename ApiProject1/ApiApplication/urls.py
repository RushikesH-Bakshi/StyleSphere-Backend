from django.urls import path
from .import views

urlpatterns=[
    path('', views.index),
    path('show/', views.get_data),
    path('login/', views.login.as_view(), name='login'),
    path('chat/', views.generateImage.as_view(), name='chat'),
    path('user/', views.getUserProfile.as_view(), name='user'),
    path('register/', views.AddUser.as_view(), name='add_user'),
    path('test/', views.test_endpoint, name='test_endpoint')
]
