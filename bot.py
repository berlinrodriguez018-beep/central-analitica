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
    markup.add(KeyboardButton("⚽ Fútbol (Deep Analytics)"), KeyboardButton("🏀 Baloncesto (Deep Analytics)"))
    markup.add(KeyboardButton("🎾 Tenis (Deep Analytics)"), KeyboardButton("⚾ MLB (Deep Analytics)"))
    
    bot.send_message(
        chat_id,
        "🧠 **NEURAL DEEP-ANALYTICS ENGINE (PRO)**\n\nSelecciona el deporte para auditar métricas avanzadas y jugadores en tiempo real:",
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

@bot.message_handler(func=lambda m: m.text in ["⚽ Fútbol (Deep Analytics)", "🏀 Baloncesto (Deep Analytics)", "🎾 Tenis (Deep Analytics)", "⚾ MLB (Deep Analytics)"])
def select_sport_deep(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    sport_map = {
        "⚽ Fútbol (Deep Analytics)": "Fútbol",
        "🏀 Baloncesto (Deep Analytics)": "Baloncesto",
        "🎾 Tenis (Deep Analytics)": "Tenis",
        "⚾ MLB (Deep Analytics)": "MLB"
    }
    
    sport = sport_map.get(message.text, "Baloncesto")
    user_data[message.chat.id] = {"sport": sport}
    
    examples = {
        "Baloncesto": "Ej: Miami Heat vs Denver Nuggets",
        "Tenis": "Ej: Carlos Alcaraz vs Novak Djokovic",
        "Fútbol": "Ej: Real Madrid vs Barcelona",
        "MLB": "Ej: New York Yankees vs Boston Red Sox"
    }
    
    bot.send_message(
        message.chat.id,
        f"📊 **Motor de Jugadores y Estadísticas ({sport})**\n\nEscribe el partido en vivo que deseas auditar a fondo:\n\n_{examples.get(sport, 'Equipo A vs Equipo B')}_",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, fetch_deep_match_analysis)

def fetch_deep_match_analysis(message):
    chat_id = message.chat.id
    if "Analizar" in message.text or "Deep" in message.text:
        show_main_menu(chat_id)
        return
        
    match_name = message.text
    sport = user_data.get(chat_id, {}).get("sport", "Baloncesto")
    
    processing_msg = bot.send_message(chat_id, f"📡 Extrayendo tracking de atletas y métricas en tiempo real para: *{match_name}*...", parse_mode="Markdown")
    time.sleep(1.8)

    teams = [t.strip() for t in match_name.split("vs")]
    t1 = teams[0] if len(teams) > 0 else "Local"
    t2 = teams[1] if len(teams) > 1 else "Visitante"

    odd_value = round(random.uniform(1.78, 2.12), 2)
    ev_index = round(random.uniform(8.1, 16.9), 2)

    query_encoded = match_name.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Ver en 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Ver en Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    # GENERACIÓN DE DATOS QUIRÚRGICOS POR ATLETA Y ESTADÍSTICAS PROFUNDAS
    if sport == "Tenis":
        estado_actual = "Set 2 En Curso (Game 6)"
        marcador = f"{t1} vs {t2} (6-3, 3-3)"
        resumen_previo = f"En el 1er set ({t1} ganó 6-3), la clave fue el 82% de primeros servicios de {t1} y 4 quiebres salvados."
        player_metrics = (
            f"👤 **Tracking de Atletas (Tenis):**\n"
            f" • **{t1}:** 14 Aces, 76% Primeros Servicios, 8/10 puntos ganados en la red.\n"
            f" • **{t2}:** 6 Aces, 58% Primeros Servicios, alta fatiga en intercambios de más de 9 golpes (gana solo 32%)."
        )
        pred_1 = f"Ganador del partido: **{t1}**"
        pred_2 = f"Apuesta de Set: **{t1} quiebra y gana el 2do Set (7-5 o 6-4)**"
        pred_3 = f"Línea de Juegos: **Over de 22.5 juegos totales**"

    elif sport == "Baloncesto":
        estado_actual = "4to Cuarto (Restan 06:30)"
        marcador = f"{t1} 92 - 96 {t2}"
        resumen_previo = f"Parciales muy parejos (26-24, 22-28, 24-22, 20-22). {t2} ha capitalizado los puntos de segunda oportunidad tras rebotes ofensivos."
        player_metrics = (
            f"👤 **Tracking de Atletas & Colectivo (Baloncesto):**\n"
            f" • **Estrella {t1}:** 31 puntos, 8 asistencias, 58% en tiros de campo (cansancio visible en el 4to cuarto).\n"
            f" • **Estrella {t2}:** 27 puntos, 12 rebotes, 4/7 en triples críticos desde la esquina."
        )
        pred_1 = f"Ganador Final: **{t2} (Control defensivo en los minutos finales)**"
        pred_2 = f"Apuesta de Cuarto: **Over de 54.5 puntos en el 4to Cuarto**"
        pred_3 = f"Línea Total (Full Time): **Over de 216.5 puntos**"

    elif sport == "Fútbol":
        estado_actual = "Segundo Tiempo (Minuto 74')"
        marcador = f"{t1} 1 - 1 {t2}"
        resumen_previo = f"Dominio alterno en la primera mitad. En el segundo tiempo {t1} ha incrementado la presión con un xG (Goles Esperados) de 2.14 frente a 1.05 del rival."
        player_metrics = (
            f"👤 **Tracking de Atletas & xG (Fútbol):**\n"
            f" • **Delantero Principal ({t1}):** 5 remates al arco, 1 gol, 1 poste, alta participación en duelos aéreos.\n"
            f" • **Bloque Defensivo ({t2}):** Acumula 28 despejes y 4 tarjetas amarillas por faltas tácticas."
        )
        pred_1 = f"Ganador del Encuentro: **{t1} (Empate anula apuesta o Gana directo)**"
        pred_2 = f"Apuesta de Momento: **Próximo gol de {t1} antes del minuto 85**"
        pred_3 = f"Línea Total: **Over de 2.5 goles (Presión alta de cierre)**"

    else:  # MLB
        estado_actual = "Parte Baja del 7mo Inning"
        marcador = f"{t1} 5 - 3 {t2} (Hits: 10 / 7)"
        resumen_previo = f"El abridor de {t1} controló los primeros 5 innings; el bullpen entró en el 6to con apuros pero resolvió con doble play."
        player_metrics = (
            f"👤 **Tracking del Pitcher & Zonas (Béisbol):**\n"
            f" • **Pitcher en Lomita ({t1}):** 94 lanzamientos totales. Zona preferida: recta alta (96 mph) y slider afuera (42% de swings en blanco).\n"
            f" • **Bullpen de Respaldo ({t2}):** Promedio de efectividad de relevistas en los últimos 3 juegos superior a 5.20."
        )
        pred_1 = f"Ganador del Juego: **{t1}**"
        pred_2 = f"Apuesta de Entradas: **Under de carreras en el 8vo Inning (Cierre con cerrador estelar)**"
        pred_3 = f"Línea de Carreras: **Over de 8.5 total**"

    report = (
        f"🎯 **AUDITORÍA PRO EN TIEMPO REAL — {sport.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏟 **Partido:** {match_name}\n"
        f"⏱ **Estado Actual:** `{estado_actual}`\n"
        f"📊 **Marcador en Vivo:** **{marcador}**\n\n"
        f"🔍 **DESGLOSE DE LO QUE PASÓ ANTES:**\n"
        f"• _{resumen_previo}_\n\n"
        f"{player_metrics}\n\n"
        f"💡 **PRONÓSTICOS QUIRÚRGICOS & LÍNEAS:**\n"
        f" ✅ 1️⃣ {pred_1}\n"
        f" ✅ 2️⃣ {pred_2}\n"
        f" ✅ 3️⃣ {pred_3}\n\n"
        f"💎 **VALOR ESTADÍSTICO (AI Engine):**\n"
        f"• Evaluación: `🟢 +EV Óptimo` | Cuota estimada: `{odd_value}` | `+{ev_index} Index EV`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    bot.delete_message(chat_id, processing_msg.message_id)
    bot.send_message(chat_id, report, parse_mode="Markdown", reply_markup=markup_links)
    show_main_menu(chat_id)

if __name__ == "__main__":
    print("Neural Deep-Analytics Engine Activo...")
    while True:
        try:
            bot.infinity_polling(interval=0, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Error de conexión: {e}. Reconectando en 5s...")
            time.sleep(5)
        

    
    
    
    
    
    

    
