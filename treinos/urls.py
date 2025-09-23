from django.urls import path
from . import views

urlpatterns = [
    path('listar_treinos/', views.listar_treinos_view, name="listar_treinos"),
    path('listar_treino_exercicios/<int:treino_id>/', views.listar_treino_exercicios, name="listar_treino_exercicios")
]