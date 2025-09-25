from django.db import models
from exercicios.models import Exercicio

class Treino(models.Model):
    nome_treino = models.CharField(max_length=150)
    descricao_treino = models.TextField()
    url_imagem_treino = models.URLField(null=True, blank=True)
    exercicios = models.ManyToManyField(Exercicio, through='TreinoExercicio', related_name='treinos')

    def __str__(self):
        return self.nome_treino


class TreinoExercicio(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('treino', 'exercicio')

    def __str__(self):
        return self.treino.nome_treino
