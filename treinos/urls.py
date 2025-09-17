from django.urls import path
from . import views

urlpatterns = [
    path('ver_treinos/', views.ver_treino, name="ver_treino"),
    path('inserir_treino/', views.inserir_treino, name="inserir_treino")
]