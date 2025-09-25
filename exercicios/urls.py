from django.urls import path
from . import views

urlpatterns = [
    path('ver_exercicio/<int:exercicio_id>/', views.ver_exercicio_view, name='ver_exercicio')
]