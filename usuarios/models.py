import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from treinos.models import Treino


class UsuarioManager(BaseUserManager):
    def create_user(self, email_usuario, nome_usuario, senha_usuario, data_nascimento):
        if not email_usuario:
            raise ValueError("Email é obrigatório")
        email_usuario = self.normalize_email(email_usuario)
        user = self.model(
            email_usuario=email_usuario,
            nome_usuario=nome_usuario,
            data_nascimento=data_nascimento
        )
        user.set_password(senha_usuario)  # hash automático
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_usuario = models.CharField(max_length=150)
    email_usuario = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email_usuario'
    REQUIRED_FIELDS = ['nome_usuario']

    objects = UsuarioManager()

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