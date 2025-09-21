import json
import uuid

from rest_framework.decorators import api_view
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from utils.get_user_from_token import get_user_from_token
from .models import Treino, Usuario, UsuarioTreino, UsuarioExercicio

from django.http import JsonResponse


@api_view(['POST'])
def criar_usuario(request):
    try:
        data = json.loads(request.body)
        nome = data.get("nome_usuario")
        email = data.get("email_usuario")
        senha = data.get("senha_usuario")
        nascimento = data.get("data_nascimento")

        if not all([nome, email, senha, nascimento]):
            return JsonResponse({"result": None, "error": "Todos os campos são obrigatórios"}, status=400)

        if Usuario.objects.filter(email_usuario=email).exists():
            return JsonResponse({"result": None, "error": "Email já cadastrado"}, status=400)

        usuario = Usuario.objects.create_user(
            nome_usuario=nome,
            email_usuario=email,
            password=senha,
            data_nascimento=nascimento
        )

        return JsonResponse({
            "result": {
                "message": "Usuário criado com sucesso",
                "usuario": {
                    "id": str(usuario.id),
                    "nome": usuario.nome_usuario,
                    "email": usuario.email_usuario,
                    "data_nascimento": str(usuario.data_nascimento)
                }
            },
            "error": None
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"result": None, "error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"result": None, "error": str(e)}, status=500)


@api_view(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body)
        email = data.get("email_usuario")
        senha = data.get("senha_usuario")
    except json.JSONDecodeError:
        return JsonResponse({"result": None, "error": "JSON inválido"}, status=400)

    if not all([email, senha]):
        return JsonResponse({"result": None, "error": "Email e senha são obrigatórios"}, status=400)

    try:
        usuario = Usuario.objects.get(email_usuario=email)
    except Usuario.DoesNotExist:
        return JsonResponse({"result": None, "error": "Usuário ou senha inválidos"}, status=404)

    if usuario.check_password(senha):
        refresh = RefreshToken.for_user(usuario)

        refresh['jti'] = str(uuid.uuid4())
        return JsonResponse({
            "result": {
                "message": "Login realizado com sucesso",
                "usuario": {
                    "id": str(usuario.id),
                    "nome": usuario.nome_usuario,
                    "email": usuario.email_usuario
                },
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
            },
            "error": None
        })

    return JsonResponse({"result": None, "error": "Usuário ou senha inválidos"}, status=401)


@api_view(['POST'])
def refresh_token_view(request):
    try:
        data = json.loads(request.body)
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            return JsonResponse({"result": None, "error": "Refresh token obrigatório"}, status=400)

        try:
            token = RefreshToken(refresh_token)
            # Se usar blacklist, ele vai lançar TokenError se estiver invalidado
        except TokenError:
            return JsonResponse({"result": None, "error": "Refresh token inválido ou expirado"}, status=401)

        new_access = str(token.access_token)  # gera novo access token

        return JsonResponse({
            "result": {
                "access": new_access
            },
            "error": None
        })

    except json.JSONDecodeError:
        return JsonResponse({"result": None, "error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"result": None, "error": str(e)}, status=500)


@api_view(['POST'])
def logout_view(request):
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()  # adiciona o refresh token à blacklist
        return JsonResponse({"result": "Logout realizado com sucesso", "error": None})
    except Exception as e:
        return JsonResponse({"result": None, "error": str(e)}, status=400)


@api_view(['GET'])
def treinos_usuario_view(request):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    # Paginação
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 10))
    start = (page - 1) * size
    end = start + size

    # Filtra treinos do usuário autenticado
    treinos = UsuarioTreino.objects.filter(usuario=user).order_by("data")
    total = treinos.count()
    treinos_page = treinos[start:end]

    treinos_list = [
        {
            "id": str(treino.id),
            "nome_treino": treino.treino.nome_treino,
            "descricao_treino": treino.treino.descricao_treino,
            "imagem_treino": treino.treino.imagem_treino.url if treino.treino.imagem_treino else None,
            "data": str(treino.data),
            "treinou": treino.treinou
        }
        for treino in treinos_page
    ]

    total_pages = (total + size - 1) // size  # total de páginas
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


@api_view(['GET'])
def exercicios_usuario_treino(request, treino_id):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    try:
        treino = Treino.objects.get(id=treino_id)
    except Treino.DoesNotExist:
        return JsonResponse({"result": None, "error": "Treino não encontrado"}, status=404)

    # Pega todos os exercícios do treino
    exercicios = treino.exercicios.all()

    # Pega o status de cada exercício para o usuário
    exercicios_list = []
    for exercicio in exercicios:
        try:
            usuario_exercicio = UsuarioExercicio.objects.get(
                usuario=user,
                treino=treino,
                exercicio=exercicio
            )
            concluido = usuario_exercicio.concluido
        except UsuarioExercicio.DoesNotExist:
            concluido = False

        exercicios_list.append({
            "id": str(exercicio.id),
            "nome_exercicio": exercicio.nome_exercicio,
            "descricao_exercicio": exercicio.descricao_exercicio,
            "series": exercicio.series,
            "repeticoes": exercicio.repeticoes,
            "video_exercicio": exercicio.video_exercicio,
            "concluido": concluido
        })

    return JsonResponse({"result": exercicios_list, "error": None})


@api_view(['GET'])
def exercicios_usuario_treino_view(request, usuario_treino_id):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    try:
        usuario_treino = UsuarioTreino.objects.get(id=usuario_treino_id, usuario=user)
    except UsuarioTreino.DoesNotExist:
        return JsonResponse({"result": None, "error": "Treino do usuário não encontrado"}, status=404)

    exercicios_list = []
    for usuario_exercicio in usuario_treino.exercicios.all():
        exercicios_list.append({
            "id": str(usuario_exercicio.exercicio.id),
            "nome_exercicio": usuario_exercicio.exercicio.nome_exercicio,
            "descricao_exercicio": usuario_exercicio.exercicio.descricao_exercicio,
            "series": usuario_exercicio.exercicio.series,
            "repeticoes": usuario_exercicio.exercicio.repeticoes,
            "video_exercicio": usuario_exercicio.exercicio.video_exercicio,
            "concluido": usuario_exercicio.concluido
        })

    return JsonResponse({"result": exercicios_list, "error": None})
