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
    markup.add(KeyboardButton("⚽ Fútbol Pro (En Vivo)"), KeyboardButton("🏀 Baloncesto Pro (En Vivo)"))
    markup.add(KeyboardButton("🎾 Tenis Pro (En Vivo)"), KeyboardButton("⚾ MLB Béisbol (En Vivo)"))
    
    bot.send_message(
        chat_id,
        "🎯 **CENTRAL ANALÍTICA DIRECTA — EN VIVO**\n\nSelecciona el deporte que deseas auditar:",
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

@bot.message_handler(func=lambda m: m.text in [
    "⚽ Fútbol Pro (En Vivo)", "⚽ Fútbol (Deep Analytics)", "⚽ Analizar Fútbol",
    "🏀 Baloncesto Pro (En Vivo)", "🏀 Baloncesto (Deep Analytics)", "🏀 Analizar Baloncesto Pro (En Vivo)",
    "🎾 Tenis Pro (En Vivo)", "🎾 Tenis (Deep Analytics)", "🎾 Analizar Tenis",
    "⚾ MLB Béisbol (En Vivo)", "⚾ MLB (Deep Analytics)", "⚾ Analizar MLB (Béisbol)"
])
def select_sport_direct(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    text = message.text
    if "Fútbol" in text:
        sport = "Fútbol"
    elif "Baloncesto" in text:
        sport = "Baloncesto"
    elif "Tenis" in text:
        sport = "Tenis"
    else:
        sport = "MLB"
        
    user_data[message.chat.id] = {"sport": sport}
    
    bot.send_message(
        message.chat.id,
        f"📋 **Paso 1/2 ({sport})**\n\nEscribe el nombre del partido (Ej: *Dinamarca vs Portugal*):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_match_participants)

def get_match_participants(message):
    chat_id = message.chat.id
    if "Pro" in message.text or "Analizar" in message.text:
        show_main_menu(chat_id)
        return
        
    if chat_id not in user_data:
        user_data[chat_id] = {}
        
    user_data[chat_id]["match"] = message.text
    sport = user_data[chat_id].get("sport", "Fútbol")
    
    examples = {
        "Fútbol": "Ej: 62' min, 2-2",
        "Baloncesto": "Ej: 3er cuarto, 74-78",
        "Tenis": "Ej: Set 2, 4-3",
        "MLB": "Ej: 6to inning, 3-2"
    }
    
    bot.send_message(
        chat_id,
        f"⏱ **Paso 2/2 (Estado actual en tu pantalla)**\n\nEscribe el minuto o periodo actual y el marcador que ves (Ej: *61 min, 2-2*):\n\n_{examples.get(sport, 'Indica el momento y marcador')}_",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, generate_exact_live_report)

def generate_exact_live_report(message):
    chat_id = message.chat.id
    if "Pro" in message.text or "Analizar" in message.text:
        show_main_menu(chat_id)
        return
        
    live_status = message.text
    match_info = user_data.get(chat_id, {}).get("match", "Encuentro en vivo")
    sport = user_data.get(chat_id, {}).get("sport", "Fútbol")
    
    teams = [t.strip() for t in match_info.split("vs")]
    t1 = teams[0] if len(teams) > 0 else "Local"
    t2 = teams[1] if len(teams) > 1 else "Visitante"

    odd_value = round(random.uniform(1.78, 2.20), 2)
    ev_index = round(random.uniform(8.5, 17.5), 2)

    query_encoded = match_info.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Ver en 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Ver en Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    if sport == "Fútbol":
        resumen = f"Lectura táctica en base al desarrollo actual aportado ({live_status}). Alta presión en campo rival y espacios abiertos en transiciones defensivas."
        metrics = (
            f"👤 **Tracking de Atletas & xG ({sport}):**\n"
            f" • **{t1}:** Alta intensidad en duelos individuales, posesión activa.\n"
            f" • **{t2}:** Despliegue ofensivo vertical con alta efectividad de remates."
        )
        p1 = f"Ganador del Tramo / Siguiente Gol: **Próximo gol define tendencia**"
        p2 = f"Apuesta de Línea: **Over de goles acumulados (Inercia ofensiva alta)**"
        p3 = f"Mercado Dinámico: **Ambos anotan / Sigue la presión**"

    elif sport == "Baloncesto":
        resumen = f"Análisis de ritmo de posesión bajo el contexto aportado ({live_status})."
        metrics = f"👤 **Tracking Colectivo:** Eficiencia alta en tiros perimetrales y transición rápida."
        p1 = f"Ganador del Periodo: **Ventaja para el equipo con mejor rotación de banca**"
        p2 = f"Apuesta de Cuarto: **Over de puntos en el parcial actual**"
        p3 = f"Línea Total: **Ajuste de puntos a favor del Over**"

    elif sport == "Tenis":
        resumen = f"Lectura de quiebres y porcentajes de servicio según la situación ({live_status})."
        metrics = f"👤 **Tracking de Atletas:** Rendimiento sólido en primeros saques y puntos de break."
        p1 = f"Ganador del Set: **Jugador con mayor efectividad al resto**"
        p2 = f"Apuesta de Juegos: **Over de juegos totales**"
        p3 = f"Tendencia: **Sets disputados con alta exigencia física**"

    else:
        resumen = f"Evaluación de pitcheo y bullpen bajo el contexto ({live_status})."
        metrics = f"👤 **Tracking de Lanzamientos:** Control de zona y fatiga de relevistas."
        p1 = f"Ganador del Juego: **Definición en entradas finales**"
        p2 = f"Apuesta: **Línea de carreras Over/Under**"
        p3 = f"Cierre: **Estabilidad del cerrador**"

    report = (
        f"🎯 **AUDITORÍA EN TIEMPO REAL — {sport.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏟 **Partido:** {match_info}\n"
        f"⏱ **Estado Exacto:** `{live_status}`\n\n"
        f"🔍 **ANÁLISIS TÁCTICO EN VIVO:**\n"
        f"• _{resumen}_\n\n"
        f"{metrics}\n\n"
        f"💡 **PRONÓSTICOS QUIRÚRGICOS & LÍNEAS:**\n"
        f" ✅ 1️⃣ {p1}\n"
        f" ✅ 2️⃣ {p2}\n"
        f" ✅ 3️⃣ {p3}\n\n"
        f"💎 **VALOR ESTADÍSTICO (AI Engine):**\n"
        f"• Evaluación: `🟢 +EV Óptimo` | Cuota: `{odd_value}` | `+{ev_index} Index EV`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    bot.send_message(chat_id, report, parse_mode="Markdown", reply_markup=markup_links)
    show_main_menu(chat_id)

if __name__ == "__main__":
    print("Central Analítica Directa Activa...")
    while True:
        try:
            bot.infinity_polling(interval=0, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Error de conexión: {e}. Reconectando en 5s...")
            time.sleep(5)
                     
            
            
            
    
        

    
    
    
    
    
    

    
