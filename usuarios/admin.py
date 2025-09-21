from django.contrib import admin
from .models import Usuario, UsuarioTreino, UsuarioHistorico, UsuarioHistoricoCircunferencia

# Inline para os registros de circunferência de cada histórico
class UsuarioHistoricoCircunferenciaInline(admin.TabularInline):
    model = UsuarioHistoricoCircunferencia
    extra = 1

# Inline para os treinos do usuário
class UsuarioTreinoInline(admin.TabularInline):
    model = UsuarioTreino
    extra = 1

# Admin do usuário
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario', 'email_usuario', 'data_nascimento')
    search_fields = ('nome_usuario', 'email_usuario')
    inlines = [UsuarioTreinoInline]

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

# Admin dos treinos do usuário
@admin.register(UsuarioTreino)
class UsuarioTreinoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'treino', 'data', 'treinou')
    list_filter = ('data', 'treinou')
    search_fields = ('usuario__nome_usuario', 'treino__nome_treino')
