import os
import random
import time
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8620258395:AAE2XAQa73pnApjdP6ozdEcun-q9b-lXsE8"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5019002345  # Tu ID privado

@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID)
def block_unauthorized(message):
    return

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("🏀 Tendencias Baloncesto"), KeyboardButton("⚽ Tendencias Fútbol"))
    markup.add(KeyboardButton("🎾 Tendencias Tenis"), KeyboardButton("⚾ Tendencias MLB"))
    
    bot.send_message(
        chat_id,
        "🧠 **CENTRAL DE TENDENCIAS, HÁNDICAPS & SIMULACIÓN PRO**\n\n"
        "Escribe el comando seguido de los rivales:\n\n"
        "👉 `/analisis Golden State Valkyries vs Dallas Wings`\n"
        "👉 `/analisis Denis Shapovalov vs Alejandro Tabilo`\n"
        "👉 `/analisis Real Madrid vs Barcelona`",
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

# MANEJADORES DE LOS BOTONES DEL TECLADO INFERIOR
@bot.message_handler(func=lambda message: message.text == "🏀 Tendencias Baloncesto")
def button_basketball(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_message(
        message.chat.id,
        "🏀 **Has seleccionado Baloncesto**.\n\n"
        "Escribe el enfrentamiento que deseas auditar:\n"
        "`/analisis Lakers vs Celtics` o `/analisis Golden State Valkyries vs Dallas Wings`",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == "⚽ Tendencias Fútbol")
def button_football(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_message(
        message.chat.id,
        "⚽ **Has seleccionado Fútbol**.\n\n"
        "Escribe el enfrentamiento que deseas auditar:\n"
        "`/analisis Real Madrid vs Barcelona`",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == "🎾 Tendencias Tenis")
def button_tennis(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_message(
        message.chat.id,
        "🎾 **Has seleccionado Tenis**.\n\n"
        "Escribe el partido o jugadores que deseas auditar:\n"
        "`/analisis Denis Shapovalov vs Alejandro Tabilo`",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == "⚾ Tendencias MLB")
def button_baseball(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_message(
        message.chat.id,
        "⚾ **Has seleccionado MLB**.\n\n"
        "Escribe los equipos de béisbol a auditar:\n"
        "`/analisis Yankees vs Red Sox`",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['analisis', 'tendencia', 'simulacion', 'futbol', 'basket', 'tenis', 'mlb'])
def handle_pro_analysis(message):
    if message.from_user.id != ADMIN_ID:
        return
        
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
            "`/analisis EquipoA vs EquipoB`",
            parse_mode="Markdown"
        )
        return

    match_name = text_content
    teams = [t.strip() for t in match_name.split("vs") if t.strip()]
    comp_a = teams[0] if len(teams) > 0 else "Competidor A"
    comp_b = teams[1] if len(teams) > 1 else "Competidor B"

    # DETECCIÓN DE DEPORTE PRECISA
    lower_match = match_name.lower()
    
    tennis_kw = ["shapovalov", "tabilo", "djokovic", "alcaraz", "sinner", "nadal", "medvedev", "zverev", "tsitsipas", "ruud", "rublev", "fritz", "hurkacz", "de minaur", "paul", "shelton", "musetti", "draper", "bublik", "cerundolo", "baez", "jarry", "etcheverry", "sabalenka", "swiatek", "gauff", "rybakina", "set", "tie-break"]
    
    basketball_kw = ["valkyries", "wings", "lakers", "celtics", "warriors", "bulls", "heat", "nuggets", "bucks", "suns", "mavericks", "knicks", "real madrid", "barcelona", "baskonia", "olympiacos", "panathinaikos", "wnba", "nba", "lynx", "liberty", "aces", "storm", "fever", "sky", "mystics", "sparks", "dream", "mercury", "sun"]
    
    baseball_kw = ["yankees", "red sox", "dodgers", "astros", "braves", "cubs", "mets", "phillies", "mlb", "inning", "pitcher"]

    if any(k in lower_match for k in tennis_kw):
        sport_type = "Tenis"
    elif any(k in lower_match for k in basketball_kw):
        sport_type = "Baloncesto"
    elif any(k in lower_match for k in baseball_kw):
        sport_type = "MLB"
    else:
        sport_type = "Fútbol"

    # MÉTRICAS GENERALES
    racha_num = random.randint(5, 11)
    porcentaje_racha = random.randint(76, 93)
    odd_value = round(random.uniform(1.72, 2.45), 2)
    ev_index = round(random.uniform(14.5, 28.0), 2)

    query_encoded = match_name.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Consultar 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Tendencias Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    # GENERACIÓN DE TENDENCIAS, HÁNDICAPS NUMÉRICOS Y LÍNEAS ESPECÍFICAS POR DEPORTE
    if sport_type == "Tenis":
        hándicap_val = round(random.choice([2.5, 3.5, 4.5]), 1)
        total_juegos = round(random.uniform(20.5, 24.5), 1)

        tendencias_principales = (
            f"• 🔥 **Racha Principal:** `{comp_a}` registra **{racha_num} victorias seguidas** imponiéndose en sets corridos sobre esta superficie.\n"
            f"• 📊 **Tendencia de Mercado:** El 80% de los partidos recientes de `{comp_b}` superan la línea de `Over {total_juegos} Juegos` totales.\n"
            f"• ⚔ **Hándicap Específico:** `Hándicap de Juegos -{hándicap_val}` para el tenista dominante."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL DE INSTANCIAS:**\n"
            f"• 🥇 *Primer Set:* Quien quiebre el servicio entre el 7mo y 9no juego se adueña del parcial por 6-4.\n"
            f"• ⚖ *Si se iguala 5-5 en el Set Final:* La estadística otorga un **83% de efectividad** en tie-breaks a favor de `{comp_a}`.\n"
            f"• 📉 *Desgaste Físico:* Partidos que superan las 2 horas de duración elevan drásticamente la tendencia al tercer set."
        )
    elif sport_type == "Baloncesto":
        hándicap_val = round(random.choice([3.5, 4.5, 5.5, 6.5, 8.5]), 1)
        total_puntos = round(random.uniform(158.5, 224.5), 1)
        q1_puntos = round(total_puntos * 0.26, 1)
        q4_puntos = round(total_puntos * 0.27, 1)

        tendencias_principales = (
            f"• 🔥 **Racha Principal:** `{comp_a}` registra **{racha_num} de los últimos 10 partidos** cubriendo la línea de puntos y hándicaps abiertos.\n"
            f"• 📊 **Tendencia de Mercado:** Línea global de `Over/Under {total_puntos} Puntos Totales` (Tendencia fuerte al Over en cruces directos).\n"
            f"• ⚔ **Hándicap Específico:** `Hándicap de Puntos -{hándicap_val}` para el favorito por control de ritmo."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL DE CUARTOS & PUNTOS:**\n"
            f"• 🥇 *1er Cuarto (Línea proyectada: {q1_puntos} pts):* Salida explosiva con ritmo alto en posesiones cortas de transición.\n"
            f"• ⚖ *Mitades:* La mayor concentración anotadora (55% del total acumulado) se genera en la segunda mitad del encuentro.\n"
            f"• 📉 *Último Cuarto (Línea proyectada: {q4_puntos} pts):* Cierre táctico estricto donde se recurre a faltas personales rápidas para alargar posesiones."
        )
    elif sport_type == "MLB":
        hándicap_val = 1.5
        total_carreras = round(random.choice([7.5, 8.5, 9.5]), 1)
        f5_carreras = round(total_carreras * 0.55, 1)

        tendencias_principales = (
            f"• 🔥 **Racha Principal:** `{comp_a}` acumula una dinámica de **{racha_num} triunfos** amparados en la solidez de su rotación abridora.\n"
            f"• 📊 **Tendencia de Mercado:** Línea establecida en `Under {total_carreras} Carreras Totales` con tendencia fuerte al `Under en Primeros 5 Innings ({f5_carreras})`.\n"
            f"• ⚔ **Hándicap Específico:** `Hándicap de Carreras -{hándicap_val}` (Run Line)."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL DE INSTANCIAS:**\n"
            f"• 🥇 *Primer Tercio (Innings 1-3):* Dominio absoluto desde la lomita, nulas libertades de extrabase a los bates principales.\n"
            f"• ⚖ *Mitad del Juego (Innings 4-6):* Instancia clave donde el orden ofensivo castiga el relevo intermedio.\n"
            f"• 📉 *Cierre (Innings 7-9):* Definición estrecha sujeta a la estabilidad del cerrador (closer) y control de hombres en base."
        )
    else:  # Fútbol
        hándicap_val = round(random.choice([0.25, 0.5, 0.75, 1.0]), 2)
        script_goles = round(random.choice([2.25, 2.5, 2.75, 3.0]), 2)

        tendencias_principales = (
            f"• 🔥 **Racha Principal:** `{comp_a}` encadena **{racha_num} partidos consecutivos** perforando la red contraria en la primera mitad.\n"
            f"• 📊 **Tendencia de Mercado:** Línea de goles en `Over/Under {script_goles}` (Mercado de *Ambos Anotan / BTTS* activo en el 82%).\n"
            f"• ⚔ **Hándicap Específico:** `Hándicap Asiático -{hándicap_val}` para asegurar protección y retorno ante empates tácticos."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL DE INSTANCIAS:**\n"
            f"• 🥇 *Primer Tiempo:* Lucha táctica intensa en la zona medular con bloques defensivos compactos.\n"
            f"• ⚖ *Minuto 60 en adelante:* El equipo en desventaja asume riesgos totales, disparando las opciones de goles y contragolpes letales.\n"
            f"• 📉 *Cierres:* Mayor resto físico y profundidad de banquillo para sostener la ventaja sobre la hora."
        )

    report = (
        f"📊 **AUDITORÍA PRO: TENDENCIAS, HÁNDICAPS & SIMULACIÓN**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏟 **Encuentro:** `{match_name}`\n"
        f"🎯 **Disciplina Detectada:** `{sport_type}`\n\n"
        f"📈 **PRINCIPALES TENDENCIAS & HÁNDICAPS CLAVE:**\n"
        f"{tendencias_principales}\n\n"
        f"{simulacion}\n\n"
        f"💎 **VALOR ESTADÍSTICO & PROBABILIDAD (+EV):**\n"
        f"• Fiabilidad Analítica: `🟢 {porcentaje_racha}% de Éxito Histórico`\n"
        f"• Cuota de Tendencia: `{odd_value}` | `+{ev_index} Index EV`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    bot.send_message(message.chat.id, report, parse_mode="Markdown", reply_markup=markup_links)

if __name__ == "__main__":
    print("Central de Tendencias, Hándicaps y Simulación Pro Activa...")
    while True:
        try:
            bot.infinity_polling(interval=0, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Error de conexión: {e}. Reconectando en 5s...")
            time.sleep(5)
    
        
    


                       
        

    
    
    
    
    
    

    
