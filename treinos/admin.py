from django.contrib import admin
from .models import Treino, TreinoExercicio

# Inline para TreinoExercicio dentro do Treino
class TreinoExercicioInline(admin.TabularInline):
    model = TreinoExercicio
    extra = 1
    autocomplete_fields = ['exercicio']

@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
    list_display = ('nome_treino', 'descricao_treino')
    inlines = [TreinoExercicioInline]
    search_fields = ('nome_treino',)  # necessário para autocomplete_fields
