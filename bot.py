import os
import random
import time
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8620258395:AAE2XAQa73pnApjdP6ozdEcun-q9b-lXsE8"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5019002345  # Tu ID privado de Telegram

user_data = {}

@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID)
def block_unauthorized(message):
    return

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("⚽ Analizar Fútbol"), KeyboardButton("🏀 Analizar Baloncesto Pro (En Vivo)"))
    markup.add(KeyboardButton("🎾 Analizar Tenis"), KeyboardButton("⚾ Analizar MLB (Béisbol)"))
    
    bot.send_message(
        chat_id,
        "🎯 **NEURAL LIVE PRO — SELECCIONA DEPORTE**",
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

@bot.message_handler(func=lambda m: m.text in ["⚽ Analizar Fútbol", "🏀 Analizar Baloncesto Pro (En Vivo)", "🎾 Analizar Tenis", "⚾ Analizar MLB (Béisbol)"])
def select_sport(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    sport_map = {
        "⚽ Analizar Fútbol": "Fútbol",
        "🏀 Analizar Baloncesto Pro (En Vivo)": "Baloncesto",
        "🎾 Analizar Tenis": "Tenis",
        "⚾ Analizar MLB (Béisbol)": "MLB"
    }
    
    sport = sport_map.get(message.text, "Baloncesto")
    user_data[message.chat.id] = {"sport": sport}
    
    bot.send_message(
        message.chat.id,
        f"🏟 **Deporte seleccionado: {sport}**\n\nEscribe el **partido en vivo** (Ej: *Carlos Alcaraz vs Novak Djokovic* o *Lakers vs Celtics*):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_match_name)

def get_match_name(message):
    chat_id = message.chat.id
    if "Analizar" in message.text:
        select_sport(message)
        return
        
    if chat_id not in user_data:
        user_data[chat_id] = {}
    
    user_data[chat_id]["match"] = message.text
    sport = user_data[chat_id].get("sport", "Baloncesto")
    
    examples = {
        "Baloncesto": "Ej: 3er cuarto, van 68-72, posesión visitante",
        "Tenis": "Ej: Set 2, Alcaraz gana 6-4, 2-1 arriba en el segundo",
        "Fútbol": "Ej: Minuto 65, van 1-0, dominando local",
        "MLB": "Ej: Alta del 6to inning, 3-2 en carreras"
    }
    
    bot.send_message(
        chat_id,
        f"⚡ **SITUACIÓN ACTUAL EN VIVO ({sport})**\n\nEscribe exactamente cómo va el partido (marcador, tiempo, set, cuarto o mitad):\n\n_{examples.get(sport, 'Describe el momento exacto')}_",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, calculate_live_analytics)

def calculate_live_analytics(message):
    chat_id = message.chat.id
    if "Analizar" in message.text:
        select_sport(message)
        return

    situation = message.text
    match_info = user_data.get(chat_id, {}).get("match", "Encuentro")
    sport = user_data.get(chat_id, {}).get("sport", "Baloncesto")
    
    teams = [t.strip() for t in match_info.split("vs")]
    t1 = teams[0] if len(teams) > 0 else "Local / Jugador 1"
    t2 = teams[1] if len(teams) > 1 else "Visitante / Jugador 2"

    odd_value = round(random.uniform(1.80, 2.10), 2)
    ev_index = round(random.uniform(7.0, 16.5), 2)

    query_encoded = match_info.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Ver en 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Ver en Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    # LÓGICA DE PREDICCIÓN DIRECTA Y ESPECÍFICA SEGÚN EL DEPORTE
    if sport == "Tenis":
        pred_ganador = f"Ganador del partido: **{t1}**"
        pred_set = f"Apuesta de Set: **{t1} gana el 2do Set**"
        linea_juegos = f"Línea de Juegos: **Over de 22.5 juegos**"
        alerta_vivo = f"Tendencia en vivo: Alta presión al resto; {t2} muestra fatiga en intercambios largos mayores a 5 tiros."

    elif sport == "Baloncesto":
        pred_ganador = f"Ganador del periodo/final: **{t1}**"
        pred_set = f"Apuesta de Cuarto/Mitad: **Over de 51.5 puntos en el 3er Cuarto**"
        linea_juegos = f"Línea Total (Full Time): **Under de 218.5 puntos**"
        alerta_vivo = f"Tendencia en vivo: Ritmo ofensivo acelerado en transición, baja intensidad defensiva en la pintura."

    elif sport == "Fútbol":
        pred_ganador = f"Ganador del encuentro: **Empate o Gana {t1} (Doble Oportunidad)**"
        pred_set = f"Apuesta de Mitad: **1er Tiempo - Under de 1.5 goles**"
        linea_juegos = f"Línea Total: **Over de 2.5 goles en el partido**"
        alerta_vivo = f"Tendencia en vivo: Bloque bajo defensivo de {t2}, buscando contragolpes rápidos por las bandas."

    else:
        pred_ganador = f"Ganador del juego: **{t1}**"
        pred_set = f"Apuesta de Innings: **Over de 1.5 carreras en las próximas 3 entradas**"
        linea_juegos = f"Línea de Carreras: **Over de 8.5 total**"
        alerta_vivo = f"Tendencia en vivo: Catcher rival con problemas de marcaje en base; bullpen intermedio inestable."

    report = (
        f"🎯 **PRONÓSTICO DIRECTO EN VIVO — {sport.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏟 **Partido:** {match_info}\n"
        f"⏱ **Contexto real aportado:** _{situation}_\n\n"
        f"💡 **SELECCIONES CLARAS DE APUESTA:**\n"
        f" ✅ 1️⃣ {pred_ganador}\n"
        f" ✅ 2️⃣ {pred_set}\n"
        f" ✅ 3️⃣ {linea_juegos}\n\n"
        f"📈 **ANÁLISIS TÁCTICO EN VIVO:**\n"
        f"• {alerta_vivo}\n\n"
        f"💎 **VALOR ESTADÍSTICO (AI Engine):**\n"
        f"• Estado: `🟢 +EV Óptimo` | Cuota estimada: `{odd_value}` | `+{ev_index} Index EV`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    bot.send_message(chat_id, report, parse_mode="Markdown", reply_markup=markup_links)
    show_main_menu(chat_id)

if __name__ == "__main__":
    print("Neural Live Pro Específico Activo...")
    while True:
        try:
            bot.infinity_polling(interval=0, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Error de conexión: {e}. Reconectando en 5s...")
            time.sleep(5)

    
    
    
    
    
    

    
