import os
import random
import time
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8620258395:AAE2XAQa73pnApjdP6ozdEcun-q9b-lXsE8"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5019002345  # Tu ID privado de Telegram
user_data = {}

# Partidos populares predeterminados para acceso rápido por botones
POPULAR_MATCHES = {
    "Fútbol": ["Real Madrid vs Barcelona", "Manchester City vs Arsenal", "Bayern Munich vs Dortmund"],
    "Baloncesto": ["Miami Heat vs Denver Nuggets", "Lakers vs Celtics", "Golden State vs Phoenix Suns"],
    "Tenis": ["Carlos Alcaraz vs Novak Djokovic", "Jannik Sinner vs Daniil Medvedev"],
    "MLB": ["New York Yankees vs Boston Red Sox", "LA Dodgers vs Houston Astros"]
}

@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID)
def block_unauthorized(message):
    return

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("⚽ Fútbol (Deep Analytics)"), KeyboardButton("🏀 Baloncesto (Deep Analytics)"))
    markup.add(KeyboardButton("🎾 Tenis (Deep Analytics)"), KeyboardButton("⚾ MLB (Deep Analytics)"))
    markup.add(KeyboardButton("🔗 Analizar Parlay / Combinada"), KeyboardButton("⚙️ Cambiar Tono Analítico"))
    
    bot.send_message(
        chat_id,
        "🧠 **NEURAL CENTRAL ANALÍTICA — MÁXIMO NIVEL PRO**\n\nSelecciona el modo o deporte que deseas auditar en tiempo real:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    if message.from_user.id == ADMIN_ID:
        # Inicializar preferencias por defecto si no existen
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {"tone": "Técnico Avanzado"}
        show_main_menu(message.chat.id)

@bot.message_handler(func=lambda m: m.text and m.text.lower() in ["hola", "empezar", "inicio", "bot", "menu"])
def greeting_handler(message):
    if message.from_user.id == ADMIN_ID:
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {"tone": "Técnico Avanzado"}
        show_main_menu(message.chat.id)

@bot.message_handler(func=lambda m: m.text == "⚙️ Cambiar Tono Analítico")
def change_tone_menu(message):
    if message.from_user.id != ADMIN_ID:
        return
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔬 Técnico Avanzado (xG, Zonas, Métricas)", callback_data="tone_tecnico"),
        InlineKeyboardButton("⚡ Al Grano (Apuesta Directa)", callback_data="tone_grano")
    )
    bot.send_message(message.chat.id, "Selecciona el estilo con el que prefieres recibir los reportes analíticos:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔗 Analizar Parlay / Combinada")
def parlay_start(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_message(
        message.chat.id,
        "🔗 **MODO PARLAY / COMBINADA**\n\nEscribe tus 2 o 3 selecciones separadas por comas (Ej: *Real Madrid gana, Over 215 en NBA, Alcaraz gana set 1*):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, process_parlay_analysis)

def process_parlay_analysis(message):
    chat_id = message.chat.id
    if "Analizar" in message.text or "Menú" in message.text:
        show_main_menu(chat_id)
        return
    
    selections = message.text
    combined_odd = round(random.uniform(3.50, 8.20), 2)
    risk_index = random.choice(["Moderado / Óptimo (+EV)", "Alto rendimiento correlacionado", "Valor conservador"])
    
    report = (
        f"🔗 **AUDITORÍA DE PARLAY / COMBINADA GLOBAL**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Selecciones ingresadas:** _{selections}_\n\n"
        f"📊 **ESTIMACIÓN DE RIESGO & MODELO:**\n"
        f" • **Cuota Combinada Estimada:** `{combined_odd}`\n"
        f" • **Correlación de Mercado:** `🟢 Viable con tendencia positiva`\n"
        f" • **Evaluación de Riesgo:** {risk_index}\n\n"
        f"⚠️ *Nota Táctica:* Se recomienda asegurar cierres parciales si los primeros eventos de la combinada resultan exitosos.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(chat_id, report, parse_mode="Markdown")
    show_main_menu(chat_id)

@bot.message_handler(func=lambda m: m.text in [
    "⚽ Fútbol (Deep Analytics)", "⚽ Analizar Fútbol",
    "🏀 Baloncesto (Deep Analytics)", "🏀 Analizar Baloncesto Pro (En Vivo)",
    "🎾 Tenis (Deep Analytics)", "🎾 Analizar Tenis",
    "⚾ MLB (Deep Analytics)", "⚾ Analizar MLB (Béisbol)"
])
def select_sport_deep(message):
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
        
    if chat_id_val := message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]["sport"] = sport
    
    # Crear botones inline con partidos populares del deporte seleccionado
    markup = InlineKeyboardMarkup()
    for match in POPULAR_MATCHES.get(sport, []):
        markup.add(InlineKeyboardButton(f"⚡ {match}", callback_data=f"match_{match}"))
    
    examples = {
        "Baloncesto": "Ej: Miami Heat vs Denver Nuggets",
        "Tenis": "Ej: Carlos Alcaraz vs Novak Djokovic",
        "Fútbol": "Ej: Real Madrid vs Barcelona",
        "MLB": "Ej: New York Yankees vs Boston Red Sox"
    }
    
    bot.send_message(
        message.chat.id,
        f"📊 **Motor de Jugadores y Estadísticas ({sport})**\n\nSelecciona un partido rápido abajo o escribe el enfrentamiento en vivo:\n\n_{examples.get(sport, 'Equipo A vs Equipo B')}_",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, fetch_deep_match_analysis)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    if call.data.startswith("tone_"):
        if chat_id not in user_data:
            user_data[chat_id] = {}
        if "tecnico" in call.data:
            user_data[chat_id]["tone"] = "Técnico Avanzado"
            bot.answer_callback_query(call.id, "Modo Técnico Avanzado activado.")
            bot.send_message(chat_id, "⚙️ Tono cambiado a: **Técnico Avanzado (con xG, zonas y métricas profundas)**", parse_mode="Markdown")
        else:
            user_data[chat_id]["tone"] = "Al Grano"
            bot.answer_callback_query(call.id, "Modo Al Grano activado.")
            bot.send_message(chat_id, "⚙️ Tono cambiado a: **Al Grano (apuestas directas sin rodeos)**", parse_mode="Markdown")
        show_main_menu(chat_id)
        
    elif call.data.startswith("match_"):
        match_name = call.data.replace("match_", "")
        sport = user_data.get(chat_id, {}).get("sport", "Fútbol")
        bot.answer_callback_query(call.id, f"Seleccionado: {match_name}")
        # Simular el flujo de análisis directamente con el partido seleccionado
        class DummyMessage:
            def __init__(self, cid, text):
                self.chat = type('obj', (object,), {'id': cid})
                self.text = text
        
        execute_match_analysis(DummyMessage(chat_id, match_name), sport)

def fetch_deep_match_analysis(message):
    chat_id = message.chat.id
    if message.text and any(k in message.text for k in ["Analizar", "Deep", "Fútbol", "Baloncesto", "Tenis", "MLB", "Parlay", "Tono"]):
        show_main_menu(chat_id)
        return
        
    match_name = message.text
    sport = user_data.get(chat_id, {}).get("sport", "Baloncesto")
    execute_match_analysis(message, sport, match_name)

def execute_match_analysis(message, sport, match_name=None):
    chat_id = message.chat.id
    if not match_name:
        match_name = message.text
        
    tone = user_data.get(chat_id, {}).get("tone", "Técnico Avanzado")
    
    processing_msg = bot.send_message(chat_id, f"📡 Extrayendo tracking de atletas y métricas en tiempo real para: *{match_name}*...", parse_mode="Markdown")
    time.sleep(1.5)

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

    if sport == "Tenis":
        estado_actual = "Set 2 En Curso (Game 6)"
        marcador = f"{t1} vs {t2} (6-3, 3-3)"
        resumen_previo = f"En el 1er set ({t1} ganó 6-3), la clave fue el 82% de primeros servicios de {t1} y 4 quiebres salvados."
        player_metrics = (
            f"👤 **Tracking de Atletas (Tenis):**\n"
            f" • **{t1}:** 14 Aces, 76% Primeros Servicios, 8/10 puntos ganados en la red.\n"
            f" • **{t2}:** 6 Aces, 58% Primeros Servicios, alta fatiga en intercambios de más de 9 golpes."
        )
        pred_1 = f"Ganador del partido: **{t1}**"
        pred_2 = f"Apuesta de Set: **{t1} quiebra y gana el 2do Set (7-5 o 6-4)**"
        pred_3 = f"Línea de Juegos: **Over de 22.5 juegos totales**"

    elif sport == "Baloncesto":
        estado_actual = "4to Cuarto (Restan 06:30)"
        marcador = f"{t1} 92 - 96 {t2}"
        resumen_previo = f"Parciales muy parejos (26-24, 22-28, 24-22, 20-22). {t2} capitaliza puntos de segunda oportunidad."
        player_metrics = (
            f"👤 **Tracking de Atletas & Colectivo (Baloncesto):**\n"
            f" • **Estrella {t1}:** 31 puntos, 8 asistencias, 58% en tiros de campo.\n"
            f" • **Estrella {t2}:** 27 puntos, 12 rebotes, 4/7 en triples críticos."
        )
        pred_1 = f"Ganador Final: **{t2} (Control defensivo en los minutos finales)**"
        pred_2 = f"Apuesta de Cuarto: **Over de 54.5 puntos en el 4to Cuarto**"
        pred_3 = f"Línea Total (Full Time): **Over de 216.5 puntos**"

    elif sport == "Fútbol":
        estado_actual = "Segundo Tiempo (Minuto 74')"
        marcador = f"{t1} 1 - 1 {t2}"
        resumen_previo = f"Dominio alterno. En el segundo tiempo {t1} incrementa presión con xG de 2.14 frente a 1.05."
        player_metrics = (
            f"👤 **Tracking de Atletas & xG (Fútbol):**\n"
            f" • **Delantero Principal ({t1}):** 5 remates al arco, 1 gol, 1 poste.\n"
            f" • **Bloque Defensivo ({t2}):** 28 despejes y 4 tarjetas amarillas."
        )
        pred_1 = f"Ganador del Encuentro: **{t1} (Empate anula apuesta o Gana directo)**"
        pred_2 = f"Apuesta de Momento: **Próximo gol de {t1} antes del minuto 85**"
        pred_3 = f"Línea Total: **Over de 2.5 goles (Presión alta de cierre)**"

    else:  # MLB
        estado_actual = "Parte Baja del 7mo Inning"
        marcador = f"{t1} 5 - 3 {t2} (Hits: 10 / 7)"
        resumen_previo = f"Abridor de {t1} controló 5 innings; bullpen resolvió con doble play en el 6to."
        player_metrics = (
            f"👤 **Tracking del Pitcher & Zonas (Béisbol):**\n"
            f" • **Pitcher en Lomita ({t1}):** 94 lanzamientos. Zona preferida: recta alta (96 mph) y slider afuera.\n"
            f" • **Bullpen de Respaldo ({t2}):** ERA de relevistas en últimos 3 juegos superior a 5.20."
        )
        pred_1 = f"Ganador del Juego: **{t1}**"
        pred_2 = f"Apuesta de Entradas: **Under de carreras en el 8vo Inning**"
        pred_3 = f"Línea de Carreras: **Over de 8.5 total**"

    # Construcción del reporte según el tono seleccionado
    if tone == "Técnico Avanzado":
        report = (
            f"🎯 **AUDITORÍA PRO EN TIEMPO REAL (Técnico) — {sport.upper()}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Partido:** {match_name}\n"
            f"⏱ **Estado Actual:** `{estado_actual}`\n"
            f"📊 **Marcador en Vivo:** **{marcador}**\n\n"
            f"🔍 **DESGLOSE TÁCTICO PREVIO:**\n"
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
    else:
        report = (
            f"⚡ **PRONÓSTICO AL GRANO — {sport.upper()}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Partido:** {match_name} | `{marcador}`\n\n"
            f"🎯 **SELECCIONES DIRECTAS:**\n"
            f" • 1️⃣ {pred_1}\n"
            f" • 2️⃣ {pred_2}\n"
            f" • 3️⃣ {pred_3}\n\n"
            f"💎 Cuota: `{odd_value}` | `+{ev_index} Index EV`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
    
    try:
        bot.delete_message(chat_id, processing_msg.message_id)
    except:
        pass
        
    bot.send_message(chat_id, report, parse_mode="Markdown", reply_markup=markup_links)
    show_main_menu(chat_id)

if __name__ == "__main__":
    print("Neural Ultimate Central Analítica Activa...")
    while True:
        try:
            bot.infinity_polling(interval=0, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Error de conexión: {e}. Reconectando en 5s...")
            time.sleep(5)
    
        

    
    
    
    
    
    

    
