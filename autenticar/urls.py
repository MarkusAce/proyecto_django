from django.urls import path
from . import views

urlpatterns = [    
    path('ingresar', views.ingresar, name="ingresar")
]