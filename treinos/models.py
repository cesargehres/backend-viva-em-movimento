from django.db import models

class Treino(models.Model):
    id_treino = models.AutoField(primary_key=True)
    nome_treino = models.CharField(max_length=150)
    descricao_treino = models.TextField()
    imagem_treino = models.CharField(max_length=150)

    def __str__(self):
        return self.nome_treino