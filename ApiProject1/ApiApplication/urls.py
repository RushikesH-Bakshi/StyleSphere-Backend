from django.urls import path
from .import views

urlpatterns=[
    path('', views.index),
    path('add/', views.AddUserView.as_view(), name='add_user'),
    path('show/', views.get_data),
]
