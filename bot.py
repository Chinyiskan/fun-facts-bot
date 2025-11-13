import os
import uuid
import asyncio
import tempfile
import requests
from gtts import gTTS
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carga variables desde el archivo .env (por ejemplo, DISCORD_TOKEN)
load_dotenv()

# Guardamos en memoria el último "fun fact" para reutilizarlo en !read
last_fact = None

def fetch_fact():
    # URL de la API pública que devuelve datos curiosos en formato JSON
    url = "https://uselessfacts.jsph.pl/random.json"
    try:
        # Hacemos la petición HTTP con un timeout para no quedar "colgados"
        resp = requests.get(url, timeout=10)
        try:
            # Intentamos parsear la respuesta como JSON y la imprimimos para fines educativos
            data = resp.json()
            print(data)
        except ValueError:
            # Si no es JSON válido, lo marcamos como None
            data = None
        # Validamos: código 200 y existencia del campo "text" con contenido
        if resp.status_code == 200 and isinstance(data, dict) and "text" in data and data["text"]:
            return data["text"]
        # Si algo falla (código no 200 o formato inesperado), devolvemos None
        return None
    except requests.exceptions.RequestException as e:
        # Capturamos errores de red (sin internet, timeout, DNS, etc.)
        print(f"HTTP error: {e}")
        return None

intents = discord.Intents.default()
# Necesario para leer el contenido de los mensajes (!start, !fact, !read)
intents.message_content = True
# Creamos el bot con prefijo "!" y los intents configurados
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="start")
async def start(ctx):
    # Muestra un saludo y el menú básico de comandos disponibles
    await ctx.send(
        "Hola 👋 Soy tu bot de fun facts.\n\n"
        "Comandos disponibles:\n"
        "• !start — muestra este menú.\n"
        "• !fact — obtiene un dato curioso y lo envía al canal.\n"
        "• !read — convierte el último dato en audio mp3 y lo adjunta.\n\n"
        "Consejo: si aún no hay un fact, !read lo obtiene automáticamente."
    )

@bot.command(name="fact")
async def fact(ctx):
    # Obtiene un fun fact desde la API y lo guarda en cache
    global last_fact
    text = fetch_fact()
    if text:
        last_fact = text
        await ctx.send(text)
    else:
        await ctx.send("No pude obtener un dato. Intenta más tarde.")

@bot.command(name="read")
async def read_cmd(ctx):
    # Convierte el último fun fact a audio y lo adjunta como mp3
    global last_fact
    # Si no hay fact previo, intentamos obtener uno nuevo
    if not last_fact:
        last_fact = fetch_fact()
    if not last_fact:
        await ctx.send("No hay dato disponible para leer.")
        return
    # gTTS genera audio (mp3) en inglés usando el texto del fact
    tts = gTTS(text=last_fact, lang="en")
    # Creamos un nombre temporal único para evitar colisiones
    tmp_name = f"fact_{uuid.uuid4().hex}.mp3"
    tmp_path = os.path.join(tempfile.gettempdir(), tmp_name)
    # Guardamos el mp3 en el directorio temporal del sistema
    tts.save(tmp_path)
    try:
        # Enviamos el archivo como adjunto al canal
        await ctx.send(file=discord.File(tmp_path, filename="fact.mp3"))
    finally:
        # Eliminamos el archivo temporal para no dejar basura en el sistema
        try:
            os.remove(tmp_path)
        except OSError:
            pass

def main():
    # Leemos el token del bot desde variables de entorno (cargadas por load_dotenv)
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Falta variable de entorno DISCORD_TOKEN")
    # Inicia el cliente y se conecta a Discord
    bot.run(token)

if __name__ == "__main__":
    # Punto de entrada del script
    main()