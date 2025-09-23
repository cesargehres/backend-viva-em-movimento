from rest_framework.decorators import api_view
from django.http import JsonResponse
from treinos.models import Treino

@api_view(['GET'])
def listar_treinos_view(request):
    # Paginação
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 10))
    start = (page - 1) * size
    end = start + size

    treinos = Treino.objects.all().order_by("nome_treino")
    total = treinos.count()
    treinos_page = treinos[start:end]

    treinos_list = [
        {
            "id_treino": treino.id,
            "nome_treino": treino.nome_treino,
            "descricao_treino": treino.descricao_treino,
            "url_imagem_treino": treino.url_imagem_treino if treino.url_imagem_treino else None,
        }
        for treino in treinos_page
    ]

    total_pages = (total + size - 1) // size
    next_page = page + 1 if page < total_pages else None
    previous_page = page - 1 if page > 1 else None

    return JsonResponse({
        "result": {
            "total_treinos": total,
            "current_page": page,
            "next_page": next_page,
            "previous_page": previous_page,
            "treinos": treinos_list
        },
        "error": None
    })


from rest_framework.decorators import api_view
from django.http import JsonResponse
from treinos.models import Treino

@api_view(['GET'])
def listar_treino_exercicios(request, treino_id):
    try:
        treino = Treino.objects.get(id=treino_id)

        exercicios_list = [
            {
                "id_exercicio": exercicio.id,
                "nome_exercicio": exercicio.nome_exercicio,
                "descricao_exercicio": exercicio.descricao_exercicio,
                "series": exercicio.series,
                "repeticoes": exercicio.repeticoes,
                "video_exercicio": exercicio.video_exercicio,
            }
            for exercicio in treino.exercicios.all()
        ]

        return JsonResponse({
            "result": {
                "id_treino": treino.id,
                "nome_treino": treino.nome_treino,
                "descricao_treino": treino.descricao_treino,
                "url_imagem_treino": treino.url_imagem_treino if treino.url_imagem_treino else None,
                "exercicios": exercicios_list,
            },
            "error": None
        })

    except Treino.DoesNotExist:
        return JsonResponse({"result": None, "error": "Treino não encontrado"}, status=404)
