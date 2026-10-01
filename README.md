# Viva em Movimento — API

API REST de um app de treinos físicos. O usuário se cadastra, escolhe treinos de um catálogo, agenda esses treinos em datas, marca cada exercício como concluído e registra a evolução do corpo (peso, altura e circunferências) ao longo do tempo.

## Stack

- **Python 3.12** + **Django 5.2**
- **Django REST Framework**
- **JWT** com `djangorestframework-simplejwt` (access + refresh token, logout com blacklist)
- **SQLite** em desenvolvimento
- **django-cors-headers** para consumo por frontend web/mobile

## Funcionalidades

- **Autenticação:** cadastro, login, renovação de token e logout com invalidação do refresh token
- **Usuário customizado:** login por e-mail e ID em UUID
- **Catálogo de treinos:** listagem paginada, busca por nome e exercícios de cada treino
- **Agenda do usuário:** inscrição em um treino numa data; os exercícios do treino são copiados automaticamente para o usuário via *signal*
- **Progresso:** marcar exercícios e treinos como concluídos
- **Histórico corporal:** peso, altura e medidas de circunferência por data
- **Isolamento de dados:** cada usuário só acessa e altera os próprios registros

## Modelo de dados

```
Exercicio ──< TreinoExercicio >── Treino
                                    │
Usuario ──< UsuarioTreino >─────────┘
   │             │
   │             └──< UsuarioExercicio >── Exercicio
   │
   └──< UsuarioHistorico ──< UsuarioHistoricoCircunferencia
```

## Como rodar localmente

```bash
git clone https://github.com/cesargehres/backend-viva-em-movimento.git
cd backend-viva-em-movimento

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

A API sobe em `http://localhost:8000`.

O repositório já inclui um banco SQLite de demonstração com 9 treinos e 12 exercícios cadastrados, para testar a API logo após clonar. Os usuários nesse banco são contas de teste:

| Perfil | E-mail | Senha |
|---|---|---|
| Usuário de teste | `cesar@gmail.com` | `teste@teste` |

Novos treinos e exercícios podem ser cadastrados pelo painel admin em `http://localhost:8000/admin/`.

## Autenticação

As rotas marcadas com 🔒 exigem o access token no cabeçalho:

```
Authorization: Bearer <access_token>
```

Todas as respostas seguem o mesmo formato:

```json
{ "result": { ... }, "error": null }
```

## Endpoints

### Usuários — `/usuarios/`

| Método | Rota | Descrição |
|---|---|---|
| POST | `criar/` | Cadastra um usuário |
| POST | `login/` | Retorna os dados do usuário e os tokens |
| POST | `refresh_token/` | Gera um novo access token |
| POST | `logout/` | Invalida o refresh token |
| GET 🔒 | `treinos_usuario/?page=1&size=10` | Lista os treinos agendados do usuário |
| GET 🔒 | `exercicios_treino_usuario/<id>/` | Exercícios de um treino agendado, com status |
| POST 🔒 | `inscrever_usuario_treino/` | Agenda um treino numa data |
| PUT 🔒 | `atualizar_status_treino/` | Marca um treino agendado como feito |
| PUT 🔒 | `atualizar_status_exercicio/` | Marca um exercício como concluído |
| POST 🔒 | `registrar_historico_usuario/` | Registra peso, altura e circunferências |
| GET 🔒 | `listar_historico_usuario/` | Lista o histórico corporal |

### Treinos — `/treinos/`

| Método | Rota | Descrição |
|---|---|---|
| GET | `listar_treinos/?page=1&size=10` | Lista paginada de treinos |
| GET | `filtrar_treinos_por_nome/?nome=peito` | Busca treinos pelo nome |
| GET | `listar_treino_exercicios/<id>/` | Detalhes de um treino e seus exercícios |

### Exercícios — `/exercicios/`

| Método | Rota | Descrição |
|---|---|---|
| GET | `ver_exercicio/<id>/` | Detalhes de um exercício |

## Exemplos

**Cadastro**

```http
POST /usuarios/criar/
Content-Type: application/json

{
  "nome_usuario": "Maria",
  "email_usuario": "maria@email.com",
  "senha_usuario": "senhaSegura123",
  "data_nascimento": "1995-04-20"
}
```

**Login**

```http
POST /usuarios/login/
Content-Type: application/json

{ "email_usuario": "maria@email.com", "senha_usuario": "senhaSegura123" }
```

```json
{
  "result": {
    "message": "Login realizado com sucesso",
    "usuario": { "id": "…", "nome": "Maria", "email": "maria@email.com", "data_nascimento": "1995-04-20" },
    "tokens": { "access": "…", "refresh": "…" }
  },
  "error": null
}
```

**Agendar treino** 🔒

```http
POST /usuarios/inscrever_usuario_treino/
Content-Type: application/json

{ "treino_id": 1, "data": "2026-10-05" }
```

**Registrar histórico** 🔒

```http
POST /usuarios/registrar_historico_usuario/
Content-Type: application/json

{
  "usuario_peso": 68.5,
  "usuario_altura": 1.70,
  "data": "2026-10-01",
  "circunferencias": [
    { "circunferencia_descricao": "Cintura", "circunferencia_medida": 74 },
    { "circunferencia_descricao": "Braço", "circunferencia_medida": 29 }
  ]
}
```

## Estrutura do projeto

```
viva_em_movimento/   configurações do Django e rotas principais
usuarios/            usuário customizado, autenticação, agenda, progresso e histórico
treinos/             catálogo de treinos
exercicios/          catálogo de exercícios
utils/               helper de autenticação JWT
```

## Autor

**César Gehres** — [github.com/cesargehres](https://github.com/cesargehres)
