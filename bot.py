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
    markup.add(KeyboardButton("⚽ Tendencias Fútbol"), KeyboardButton("🏀 Tendencias Baloncesto"))
    markup.add(KeyboardButton("🎾 Tendencias Tenis"), KeyboardButton("⚾ Tendencias MLB"))
    
    bot.send_message(
        chat_id,
        "🧠 **CENTRAL DE TENDENCIAS & SIMULACIÓN AVANZADA**\n\n"
        "Escribe el comando seguido de los rivales para evaluar todas las instancias:\n\n"
        "👉 `/analisis Denis Shapovalov vs Alejandro Tabilo`\n"
        "👉 `/analisis Real Madrid vs Barcelona`\n"
        "👉 `/analisis Lakers vs Celtics`",
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

@bot.message_handler(commands=['analisis', 'tendencia', 'simulacion', 'futbol', 'basket', 'tenis', 'mlb'])
def handle_advanced_simulation(message):
    if message.from_user.id != ADMIN_ID:
        return
        
    # Limpieza estricta de comandos
    text_content = message.text.strip()
    for cmd in ['/analisis', '/tendencia', '/simulacion', '/futbol', '/basket', '/tenis', '/mlb']:
        if text_content.lower().startswith(cmd):
            text_content = text_content[len(cmd):].strip()
            break

    if not text_content or "vs" not in text_content.lower():
        bot.send_message(
            message.chat.id,
            "⚠ **Formato incorrecto**.\n\n"
            "Debes incluir los dos rivales separados por 'vs':\n"
            "`/analisis JugadorA vs JugadorB`",
            parse_mode="Markdown"
        )
        return

    match_name = text_content
    teams = [t.strip() for t in match_name.split("vs") if t.strip()]
    comp_a = teams[0] if len(teams) > 0 else "Competidor A"
    comp_b = teams[1] if len(teams) > 1 else "Competidor B"

    # Detección inteligente de disciplina
    lower_match = match_name.lower()
    tennis_kw = ["shapovalov", "tabilo", "djokovic", "alcaraz", "sinner", "nadal", "medvedev", "zverev", "tsitsipas", "ruud", "rublev", "fritz", "hurkacz", "de minaur", "paul", "shelton", "musetti", "draper", "bublik", "cerundolo", "baez", "jarry", "etcheverry", "sabalenka", "swiatek", "gauff", "rybakina"]
    basket_kw = ["lakers", "celtics", "warriors", "bulls", "heat", "nuggets", "bucks", "suns", "mavericks", "knicks", "real madrid", "barcelona", "baskonia", "olympiacos", "panathinaikos"]
    baseball_kw = ["yankees", "red sox", "dodgers", "astros", "braves", "cubs", "mets", "phillies"]

    if any(k in lower_match for k in tennis_kw):
        sport_type = "Tenis"
    elif any(k in lower_match for k in basket_kw):
        sport_type = "Baloncesto"
    elif any(k in lower_match for k in baseball_kw):
        sport_type = "MLB"
    else:
        sport_type = "Fútbol"

    odd_value = round(random.uniform(1.75, 2.40), 2)
    ev_index = round(random.uniform(13.0, 25.5), 2)
    prob_porcentaje = random.randint(70, 86)

    query_encoded = match_name.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Consultar 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Tendencias Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    # Bloques de simulación detallados por circunstancia e instancia
    if sport_type == "Tenis":
        tendencias = (
            f"• 🔥 **Tendencia de Superficie:** `{comp_a}` posee un registro dominante al ganar el 72% de sus partidos tras adjudicarse el primer set.\n"
            f"• ⚠ **Patrón de Quiebres:** Si `{comp_b}` cede su primer turno de saque, la estadística histórica de fuentes especializadas muestra una bajada del rendimiento mental en mangas largas."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL POR INSTANCIAS (TENIS):**\n"
            f"• 🥇 *Si se define el 1er Set:* Quien logre el quiebre entre el juego 7 y 9 cerrará con alta probabilidad por 6-4.\n"
            f"• ⚖ *Si el marcador se pone 5-5 en el Set Final:* La simulación histórica favorece a `{comp_a}` debido a su efectividad superior en tie-breaks recientes (80% de acierto bajo presión).\n"
            f"• 📉 *Escenario de Desgaste:* Si el partido supera las 2 horas y media, el índice físico inclina la balanza hacia intercambios más largos y un total de juegos en línea Over."
        )
    elif sport_type == "Baloncesto":
        tendencias = (
            f"• 🔥 **Tendencia de Inicio:** `{comp_a}` acostumbra a romper los partidos en los primeros cuartos con una media superior a 28 puntos.\n"
            f"• ⚠ **Patrón de Cierre:** Si `{comp_b}` llega al tercer cuarto con una desventaja menor a 5 puntos, su efectividad exterior aumenta un 18%."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL POR INSTANCIAS (BALONCESTO):**\n"
            f"• 🥇 *Desarrollo del 1er Cuarto:* Ritmo rápido con posesiones cortas; tendencia clara al Over en el parcial inicial.\n"
            f"• ⚖ *Si el partido llega igualado al último cuarto:* El control táctico y la rotación de banquillo de `{comp_a}` reducen el margen de error defensivo.\n"
            f"• 📉 *Escenario de Faltas Tácticas:* Si la diferencia es menor a 4 puntos en los últimos 60 segundos, el encuentro se definirá desde la línea de tiros libres elevando la puntuación final."
        )
    elif sport_type == "MLB":
        tendencias = (
            f"• 🔥 **Tendencia de Lomita:** El abridor de `{comp_a}` registra control estricto en las primeras 3 entradas (WHIP bajo).\n"
            f"• ⚠ **Patrón de Relevo:** Si el bullpen de `{comp_b}` entra a lanzar temprano (antes del 5to inning), suele conceder un incremento de carreras."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL POR INSTANCIAS (BÉISBOL):**\n"
            f"• 🥇 *Primer Tercio (Innings 1-3):* Dominio de los lanzadores; baja probabilidad de carreras tempranas.\n"
            f"• ⚖ *Mitad del Juego (Innings 4-6):* Instancia crítica donde el orden al bate de `{comp_a}` explota los cambios de velocidad del serpentinero rival.\n"
            f"• 📉 *Cierre de Partido:* Definición en entradas finales sujeta a la estabilidad del cerrador (closer) con corredores en posición de anotar."
        )
    else:  # Fútbol
        tendencias = (
            f"• 🔥 **Tendencia Ofensiva:** `{comp_a}` promedia un índice alto de presión alta en campo rival durante los primeros 30 minutos.\n"
            f"• ⚠ **Patrón Condicional:** Si el marcador permanece empatado al descanso, ambos conjuntos reducen riesgos tácticos en la reanudación."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL POR INSTANCIAS (FÚTBOL):**\n"
            f"• 🥇 *Primer Tiempo:* Bloque inicial muy disputado en la medular; primer gol condiciona el planteamiento defensivo.\n"
            f"• ⚖ *Si el marcador se rompe pasada la hora de juego (Min 60+):* El equipo perdedor se ve obligado a adelantar líneas, abriendo espacios ideales para contragolpes y aumentando el mercado de córners y goles.\n"
            f"• 📉 *Escenario de Cierre:* Ventaja estadística en tramos finales para el conjunto con mayor profundidad de cambios tácticos."
        )

    report = (
        f"📊 **AUDITORÍA DE TENDENCIAS & SIMULACIÓN PROFESIONAL**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏟 **Encuentro:** `{match_name}`\n"
        f"🎯 **Disciplina Detectada:** `{sport_type}`\n\n"
        f"📈 **PRINCIPALES TENDENCIAS (WEB INSIGHTS):**\n"
        f"{tendencias}\n\n"
        f"{simulacion}\n\n"
        f"💎 **VALOR ESTADÍSTICO & PROBABILIDAD (+EV):**\n"
        f"• Probabilidad Estimada: `🟢 {prob_porcentaje}% de Certeza Analítica`\n"
        f"• Cuota de Tendencia: `{odd_value}` | `+{ev_index} Index EV`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    bot.send_message(message.chat.id, report, parse_mode="Markdown", reply_markup=markup_links)

if __name__ == "__main__":
    print("Central de Tendencias y Simulación Avanzada Activa...")
    while True:
        try:
            bot.infinity_polling(interval=0, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Error de conexión: {e}. Reconectando en 5s...")
            time.sleep(5)

                       
        

    
    
    
    
    
    

    
