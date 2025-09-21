import json
import uuid

from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from utils.get_user_from_token import get_user_from_token
from .models import Treino, Usuario, UsuarioTreino

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

    # agora você tem o user autenticado
    usuario_id = str(user.id)
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return JsonResponse({"result": None, "error": "Usuário não encontrado"}, status=404)

    treinos = UsuarioTreino.objects.filter(usuario=usuario)
    treinos_list = [
        {
            "id": str(treino.id),
            "nome_treino": treino.treino.nome_treino,
            "descricao_treino": treino.treino.descricao_treino,
            "imagem_treino": treino.treino.imagem_treino.url if treino.treino.imagem_treino else None,
            "data": str(treino.data),
            "treinou": treino.treinou
        } for treino in treinos
    ]

    return JsonResponse({"result": treinos_list, "error": None})
