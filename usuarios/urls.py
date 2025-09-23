from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('criar/', views.criar_usuario, name='criar_usuario'),
    path('refresh_token/', views.refresh_token_view, name='refresh_token'),
    path('treinos_usuario/', views.treinos_usuario_view, name='treinos_usuario'),
    path('exercicios_treino_usuario/<int:usuario_treino_id>/', views.exercicios_usuario_treino_view, name="exercicios_treino_usuario")
]
