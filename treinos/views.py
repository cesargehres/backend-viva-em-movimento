from django.http import HttpResponse
from .models import Treino

def ver_treino(request):
    return HttpResponse('Vendo produto')

def inserir_treino(request):
    return HttpResponse('Inserindo treino...')