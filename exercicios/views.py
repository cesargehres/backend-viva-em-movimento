from rest_framework.decorators import api_view
from django.http import JsonResponse
from exercicios.models import Exercicio

@api_view(['GET'])
def ver_exercicio_view(request, exercicio_id):
    try:
        exercicio = Exercicio.objects.get(id=exercicio_id)

        return JsonResponse({
            "result": {
                "id_exercicio": exercicio.id,
                "nome_exercicio": exercicio.nome_exercicio,
                "descricao_exercicio": exercicio.descricao_exercicio,
                "series": exercicio.series,
                "repeticoes": exercicio.repeticoes,
                "video_exercicio": exercicio.video_exercicio if exercicio.video_exercicio else None,
            },
            "error": None
        })

    except Exercicio.DoesNotExist:
        return JsonResponse({"result": None, "error": "Exercício não encontrado"}, status=404)
