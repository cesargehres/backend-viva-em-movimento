from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=150)
    email_usuario = models.EmailField(unique=True)
    senha_usuario = models.CharField(max_length=255)  # vamos guardar hash da senha
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome_usuario