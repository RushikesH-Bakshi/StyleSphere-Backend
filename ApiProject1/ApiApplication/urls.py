from django.urls import path
from .import views

urlpatterns=[
    path('', views.index),
    path('register/', views.AddUserView.as_view(), name='add_user'),
    path('login/', views.login.as_view(), name='login'),
    path('show/', views.get_data),
]
