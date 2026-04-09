# 🔥 Célula Moriá — Versículos

Landing page moderna para compartilhar versículos bíblicos.

## ▶️ Rodar localmente

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Criar banco de dados
python manage.py migrate

# 3. Popular versículos
python manage.py populate_versiculos

# 4. Rodar servidor
python manage.py runserver
```

Acesse: http://localhost:8000

## 📁 Arquivos estáticos

Coloque na pasta `versiculos/static/`:
- `logo.png` — logo da célula (opcional, o template não depende dela)
- `som.mp3` — som de notificação (opcional)

## 🚀 Deploy no Render

1. Suba o projeto para o GitHub
2. Crie uma conta em [render.com](https://render.com)
3. New Web Service → conectar repositório
4. Configurar:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn moria.wsgi`
5. Deploy!

## ✏️ Adicionar mais versículos

Edite o arquivo:
`versiculos/management/commands/populate_versiculos.py`

Adicione na lista `lista`:
```python
("Seu novo versículo aqui.", "Livro X:Y"),
```

Rode novamente:
```bash
python manage.py populate_versiculos
```
