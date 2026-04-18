# Célula Moriá — Site completo

Site para célula cristã com versículo da semana, pedidos de oração, reuniões e jogo interativo em tempo real.

---

## Instalação local

```bash
# 1. Clone e entre na pasta
cd moria

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env
cp .env.example .env
# Edite o .env com suas configurações

# 5. Suba o Redis (necessário para o jogo WebSocket)
docker run -d -p 6379:6379 redis:alpine
# OU instale Redis localmente: https://redis.io/download

# 6. Execute as migrações e popule as perguntas
python manage.py migrate
python manage.py popular_perguntas

# 7. Crie um superusuário para o admin
python manage.py createsuperuser

# 8. Rode o servidor
python manage.py runserver
```

Acesse: http://localhost:8000

---

## Deploy no Render (recomendado)

1. Faça push do código para o GitHub
2. No Render, clique em **New > Blueprint**
3. Conecte seu repositório
4. O `render.yaml` configura tudo automaticamente:
   - Web service com Daphne (ASGI + WebSocket)
   - PostgreSQL gratuito
   - Redis gratuito

---

## Estrutura do projeto

```
moria/
├── moria/              # Configurações Django
│   ├── settings.py
│   ├── asgi.py         # ASGI + WebSocket
│   └── urls.py
├── celula/             # App principal
│   ├── models.py       # Versículo, Reunião, Oração, Jogo
│   ├── views.py        # Views
│   ├── consumers.py    # WebSocket (jogo em tempo real)
│   ├── routing.py      # Rotas WebSocket
│   ├── admin.py        # Painel admin customizado
│   └── management/
│       └── commands/
│           └── popular_perguntas.py
├── templates/
│   ├── base.html
│   ├── celula/
│   │   ├── home.html
│   │   ├── oracao.html
│   │   └── reunioes.html
│   └── jogo/
│       ├── home.html
│       ├── sala_lider.html    # Painel do líder (WebSocket)
│       └── sala_jogador.html  # Tela do participante (WebSocket)
├── render.yaml         # Deploy automático
└── requirements.txt
```

---

## Páginas

| URL | Descrição |
|-----|-----------|
| `/` | Home com versículo, reuniões e avisos |
| `/oracao/` | Pedidos de oração |
| `/reunioes/` | Agenda de reuniões |
| `/jogo/` | Home do jogo |
| `/jogo/criar/` | Criar sala (líder) |
| `/jogo/entrar/` | Entrar na sala (participante) |
| `/jogo/sala/<codigo>/lider/` | Painel do líder |
| `/admin/` | Painel de administração |

---

## Como jogar na reunião

1. **Líder** acessa `/jogo/` no computador ou celular
2. Escolhe o tema e clica em **Criar sala**
3. Mostra o **código de 6 letras** na tela para o grupo
4. **Cada participante** acessa o site no celular, digita o código e o nome
5. Líder clica **Iniciar jogo**
6. Todos respondem no celular em tempo real
7. O líder vê os resultados e conduz a reflexão em grupo

---

## Painel Admin

Acesse `/admin/` para:
- Cadastrar versículos da semana
- Criar reuniões na agenda
- Gerenciar pedidos de oração
- Adicionar novos temas e perguntas para o jogo
- Ver salas de jogo e pontuações