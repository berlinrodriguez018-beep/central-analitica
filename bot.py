import os
import random
import time
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8620258395:AAE2XAQa73pnApjdP6ozdEcun-q9b-lXsE8"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5019002345  # Tu ID privado de Telegram

@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID)
def block_unauthorized(message):
    return

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("🏀 Simulación & Tendencias NBA"), KeyboardButton("⚽ Simulación & Tendencias Fútbol"))
    markup.add(KeyboardButton("⚾ Simulación & Tendencias MLB"), KeyboardButton("🎾 Simulación & Tendencias Tenis"))
    
    bot.send_message(
        chat_id,
        "🧠 **CENTRAL DE TENDENCIAS & SIMULACIÓN AI**\n\n"
        "Escribe el análisis que deseas generar usando este formato:\n\n"
        "👉 `/analisis Lakers vs Warriors`\n"
        "👉 `/analisis Real Madrid vs Barcelona`\n"
        "👉 `/analisis Boston Celtics vs Miami Heat`",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    if message.from_user.id == ADMIN_ID:
        show_main_menu(message.chat.id)

@bot.message_handler(func=lambda m: m.text and m.text.lower() in ["hola", "empezar", "inicio", "bot", "menu"])
def greeting_handler(message):
    if message.from_user.id == ADMIN_ID:
        show_main_menu(message.chat.id)

@bot.message_handler(commands=['analisis', 'tendencia', 'simulacion'])
def handle_trend_analysis(message):
    if message.from_user.id != ADMIN_ID:
        return
        
    text_content = message.text.replace(f"/{message.text.split()[0]}", "").strip()
    
    if not text_content:
        bot.send_message(
            message.chat.id,
            "⚠️️ **Formato incorrecto**.\n\n"
            "Debes escribir el enfrentamiento después del comando:\n"
            "`/analisis EquipoA vs EquipoB`\n\n"
            "Ejemplo: `/analisis Lakers vs Celtics`",
            parse_mode="Markdown"
        )
        return

    match_name = text_content
    teams = [t.strip() for t in match_name.split("vs")]
    team_a = teams[0] if len(teams) > 0 else "Local"
    team_b = teams[1] if len(teams) > 1 else "Visitante"

    # Generación de métricas de tendencia e índices de valor simulados
    odd_value = round(random.uniform(1.75, 2.30), 2)
    ev_index = round(random.uniform(11.0, 22.5), 2)

    query_encoded = match_name.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Buscar en Web / 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Estadísticas en Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    # Base de tendencias inteligentes simuladas orientadas a patrones reales
    tendencias_ejemplos = [
        f"🔥 **Racha Local:** `{team_a}` acumula 9 victorias consecutivas jugando en condición de local, dominando el ritmo desde el primer cuarto.",
        f"⚠️️ **Patrón Condicional:** Si `{team_b}` supera los 80 puntos al término del tercer cuarto, la tendencia histórica indica que sobrepasará la línea total porque suele complicarse defensivamente en los cierres (40 ocasiones recientes).",
        f"📉 **Efectividad Ofensiva:** En los últimos enfrentamientos directos, el promedio de anotación conjunta se eleva un 14% en la segunda mitad del encuentro."
    ]

    simulacion_resultado = (
        f"🔮 **SIMULACIÓN DE ESCENARIOS E INSTANCIAS:**\n"
        f"• *Desarrollo estimado:* Partido de alta tensión táctica con dominio alterno en los primeros parciales.\n"
        f"• *Escenario de Cierre:* Si la diferencia se mantiene por debajo de 5 puntos en el último tramo, la estadística favorece a `{team_a}` por profundidad de banquillo.\n"
        f"• *Proyección de Línea Final:* Alta probabilidad de resolución ajustada o de superar el margen Over propuesto."
    )

    report = (
        f"📊 **AUDITORÍA DE TENDENCIAS & SIMULACIÓN**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏟 **Encuentro:** `{match_name}`\n\n"
        f"📈 **PRINCIPALES TENDENCIAS DETECTADAS:**\n"
        f"• {tendencias_ejemplos[0]}\n"
        f"• {tendencias_ejemplos[1]}\n"
        f"• {tendencias_ejemplos[2]}\n\n"
        f"{simulacion_resultado}\n\n"
        f"💎 **VALOR ESTADÍSTICO & +EV (AI Engine):**\n"
        f"• Patrón Recomendado: `🟢 Alta Confiabilidad`\n"
        f"• Cuota de Tendencia: `{odd_value}` | `+{ev_index} Index EV`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    bot.send_message(message.chat.id, report, parse_mode="Markdown", reply_markup=markup_links)

if __name__ == "__main__":
    print("Central de Tendencias y Simulación Activa...")
    while True:
        try:
            bot.infinity_polling(interval=0, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Error de conexión: {e}. Reconectando en 5s...")
            time.sleep(5)
        

    
    
    
    
    
    

    
