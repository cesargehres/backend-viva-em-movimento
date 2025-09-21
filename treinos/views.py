from django.http import HttpResponse

def ver_treino(request):
    return HttpResponse('Vendo produto')

def inserir_treino(request):
    return HttpResponse('Inserindo treino...')