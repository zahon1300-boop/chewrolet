from django.urls import path
from . import views

urlpatterns = [
    path('', views.dealers_list, name='dealers_list'),
]