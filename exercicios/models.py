from django.db import models

class Exercicio(models.Model):
    nome_exercicio = models.CharField(max_length=150)
    descricao_exercicio = models.TextField()
    series = models.IntegerField()
    repeticoes = models.IntegerField()
    video_exercicio = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nome_exercicio
