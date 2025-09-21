from django.contrib import admin
from .models import (
    Usuario, UsuarioTreino, UsuarioHistorico,
    UsuarioHistoricoCircunferencia, UsuarioExercicio
)

# Inline para os registros de circunferência de cada histórico
class UsuarioHistoricoCircunferenciaInline(admin.TabularInline):
    model = UsuarioHistoricoCircunferencia
    extra = 1

# Inline para os exercícios do usuário dentro de um treino
class UsuarioExercicioInline(admin.TabularInline):
    model = UsuarioExercicio
    extra = 0
    readonly_fields = ('data',)
    autocomplete_fields = ['exercicio']

# Inline para os treinos do usuário
class UsuarioTreinoInline(admin.TabularInline):
    model = UsuarioTreino
    extra = 0
    inlines = []  # Não suporta nested inlines no Django, vamos usar UsuarioExercicioInline dentro do UsuarioTreinoAdmin

# Admin do usuário
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario', 'email_usuario', 'data_nascimento')
    search_fields = ('nome_usuario', 'email_usuario')
    inlines = [UsuarioTreinoInline]

# Admin do treino do usuário
@admin.register(UsuarioTreino)
class UsuarioTreinoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'treino', 'data', 'treinou')
    list_filter = ('data', 'treinou')
    search_fields = ('usuario__nome_usuario', 'treino__nome_treino')
    inlines = [UsuarioExercicioInline]

# Admin do histórico do usuário
@admin.register(UsuarioHistorico)
class UsuarioHistoricoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data', 'usuario_peso', 'usuario_altura')
    list_filter = ('data',)
    search_fields = ('usuario__nome_usuario',)
    inlines = [UsuarioHistoricoCircunferenciaInline]

# Admin das circunferências do histórico
@admin.register(UsuarioHistoricoCircunferencia)
class UsuarioHistoricoCircunferenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario_historico', 'get_nome_usuario', 'circunferencia_descricao', 'circunferencia_medida')
    search_fields = ('usuario_historico__usuario__nome_usuario',)

    def get_nome_usuario(self, obj):
        return obj.usuario_historico.usuario.nome_usuario
    get_nome_usuario.short_description = 'Nome do Usuário'

# Admin dos exercícios do usuário (para acesso direto)
@admin.register(UsuarioExercicio)
class UsuarioExercicioAdmin(admin.ModelAdmin):
    list_display = ('usuario_treino', 'exercicio', 'concluido', 'data')
    list_filter = ('concluido', 'data')
    search_fields = ('usuario_treino__usuario__nome_usuario', 'usuario_treino__treino__nome_treino', 'exercicio__nome_exercicio')
    ordering = ('usuario_treino', 'exercicio')
