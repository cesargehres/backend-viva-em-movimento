from django.db import models
from treinos.models import Treino

class Usuario(models.Model):
    nome_usuario = models.CharField(max_length=150)
    email_usuario = models.EmailField(unique=True)
    senha_usuario = models.CharField(max_length=255)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome_usuario


class UsuarioTreino(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    data = models.DateField()
    treinou = models.BooleanField(default=False)


class UsuarioHistorico(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    usuario_peso = models.FloatField()
    usuario_altura = models.FloatField()
    data = models.DateField()


class UsuarioHistoricoCircunferencia(models.Model):
    usuario_historico = models.ForeignKey(UsuarioHistorico, on_delete=models.CASCADE, related_name='circunferencias')
    circunferencia_descricao = models.CharField(max_length=150)
    circunferencia_medida = models.FloatField()