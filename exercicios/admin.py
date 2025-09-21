from django.contrib import admin
from .models import Exercicio

@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ('nome_exercicio', 'descricao_exercicio')  # remove 'tipo_exercicio'
    search_fields = ('nome_exercicio',)
