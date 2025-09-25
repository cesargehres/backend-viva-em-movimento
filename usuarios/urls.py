from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('criar/', views.criar_usuario, name='criar_usuario'),
    path('refresh_token/', views.refresh_token_view, name='refresh_token'),
    path('treinos_usuario/', views.treinos_usuario_view, name='treinos_usuario'),
    path('exercicios_treino_usuario/<int:usuario_treino_id>/', views.exercicios_usuario_treino_view, name="exercicios_treino_usuario"),
    path('atualizar_status_exercicio/', views.atualizar_status_exercicio_view, name='atualizar_status_exercicio'),
    path('atualizar_status_treino/', views.atualizar_usuario_treino_view, name='atualizar_status_treino'),
    path('inscrever_usuario_treino/', views.inscrever_usuario_treino_view, name='inscrever_usuario_treino'),
    path('registrar_historico_usuario/', views.criar_historico_usuario_view, name='registrar_historico_usuario'),
    path('listar_historico_usuario/', views.listar_historico_usuario_view, name='listar_historico_usuario')
]
