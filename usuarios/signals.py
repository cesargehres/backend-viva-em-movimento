from django.db.models.signals import post_save
from django.dispatch import receiver

from usuarios.models import UsuarioTreino, UsuarioExercicio
from treinos.models import TreinoExercicio


@receiver(post_save, sender=UsuarioTreino)
def criar_exercicios_usuario(sender, instance, created, **kwargs):
    """
    Ao criar um UsuarioTreino, adiciona automaticamente todos os exercícios do treino
    em UsuarioExercicio relacionados a esse UsuarioTreino.
    """
    if created:
        treino = instance.treino
        exercicios = TreinoExercicio.objects.filter(treino=treino)
        for te in exercicios:
            # Cria UsuarioExercicio apenas se não existir
            UsuarioExercicio.objects.get_or_create(
                usuario_treino=instance,
                exercicio=te.exercicio,
                defaults={'concluido': False}
            )
