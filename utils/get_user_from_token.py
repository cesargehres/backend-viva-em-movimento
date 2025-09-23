from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse

def get_user_from_token(request):
    jwt_auth = JWTAuthentication()
    try:
        result = jwt_auth.authenticate(request)
        if result is None:
            return None, JsonResponse({"result": None, "error": "Token não enviado ou inválido"}, status=401)

        user, token = result
        return user, None

    except AuthenticationFailed as e:
        return None, JsonResponse({"result": None, "error": "Token inválido"}, status=401)
    except Exception as e:
        return None, JsonResponse({"result": None, "error": "Erro ao verificar token: " + str(e)}, status=400)
