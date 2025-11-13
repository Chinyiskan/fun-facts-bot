# Discord Fun Facts Bot

Proyecto simple: bot de Discord que obtiene datos curiosos y los convierte a audio (mp3) usando gTTS.

Contenido del repo:
- `src/bot.py`: script principal del bot.
- `templates/plantilla_bot.txt`: plantilla/exercicios del bot.
- `.env.example`: ejemplo de variable de entorno requerida.
- `requirements.txt`: dependencias Python.

Cómo usar (Windows / Bash):

1. Crear y activar un entorno virtual:

```bash
python -m venv .venv
source .venv/Scripts/activate  # en Git Bash / WSL usar: source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Crear archivo `.env` en la raíz con tu token de Discord:

```
DISCORD_TOKEN=tu_token_aqui
```

4. Ejecutar el bot:

```bash
python src/bot.py
```

Notas:
- No subas tu archivo `.env` a un repo público. `.env` está en `.gitignore`.
- Para publicar en GitHub: crea un repo remoto y sigue los pasos de `git remote add` + `git push`.
