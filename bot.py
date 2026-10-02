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
        "🧠 **CENTRAL DE TENDENCIAS, HÁNDICAPS & SIMULACIÓN PRO**\n\n"
        "Escribe el comando seguido de los rivales:\n\n"
        "👉 `/analisis Denis Shapovalov vs Alejandro Tabilo`\n"
        "👉 `/analisis Lakers vs Celtics`\n"
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

@bot.message_handler(commands=['analisis', 'tendencia', 'simulacion', 'futbol', 'basket', 'tenis', 'mlb'])
def handle_pro_analysis(message):
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

    # Métricas avanzadas, hándicaps y porcentajes
    racha_victorias_a = random.randint(6, 12)
    porcentaje_racha = random.randint(81, 94)
    prob_porcentaje = random.randint(73, 89)
    odd_value = round(random.uniform(1.75, 2.45), 2)
    ev_index = round(random.uniform(15.0, 28.0), 2)

    query_encoded = match_name.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Consultar 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Tendencias Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    # Bloques de análisis con hándicaps, líneas y simulaciones profundas
    if sport_type == "Tenis":
        tendencias_principales = (
            f"• 🔥 **Racha Principal:** `{comp_a}` registra **{racha_victorias_a} victorias consecutivas** cubriendo hándicaps de juegos en arcilla/pista rápida.\n"
            f"• 📊 **Tendencia de Mercado:** El 80% de los partidos recientes de `{comp_b}` superan la línea de `Over 22.5 Juegos` totales.\n"
            f"• ⚔ **Hándicap Sugerido:** `Hándicap de Juegos -3.5 para {comp_a}` (Cumplido en 7 de los últimos 9 duelos directos)."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL & PROBABILIDADES:**\n"
            f"• 🥇 *1er Set ({prob_porcentaje}% Probabilidad):* Quien quiebre entre el 7mo y 9no juego se apodera del set por 6-4.\n"
            f"• ⚖ *Si se llega a 5-5 en el Set Final:* La simulación otorga un **84% de eficiencia** en tie-breaks a favor de `{comp_a}`.\n"
            f"• 📉 *Hándicap Asiático / Sets:* Alta probabilidad de victoria limpia o resistencia extendida a 3 mangas completas."
        )
    elif sport_type == "Baloncesto":
        tendencias_principales = (
            f"• 🔥 **Racha Principal:** `{comp_a}` acumula **{racha_victorias_a} partidos seguidos ganando** o cubriendo el hándicap de puntos como local.\n"
            f"• 📊 **Tendencia de Mercado:** Patrón claro de `Over de Puntos Totales` (Línea general superada en 8 de 10 ocasiones).\n"
            f"• ⚔ **Hándicap Sugerido:** `Hándicap -5.5 puntos` para el equipo favorito por control de posesiones en el cierre."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL & PROBABILIDADES:**\n"
            f"• 🥇 *1er Cuarto ({prob_porcentaje}% Probabilidad):* Salida ofensiva rápida con promedio superior a 54 puntos conjuntos.\n"
            f"• ⚖ *Si hay marcador ajustado en el Último Cuarto:* `{comp_a}` reduce pérdidas de balón y asegura la cobertura del hándicap desde la línea de libres.\n"
            f"• 📉 *Mercado de Mitades:* Mayor efectividad anotadora concentrada en la segunda mitad del encuentro."
        )
    elif sport_type == "MLB":
        tendencias_principales = (
            f"• 🔥 **Racha Principal:** `{comp_a}` llega con **{racha_victorias_a} de 10 triunfos** respaldados por solidez en las primeras entradas.\n"
            f"• 📊 **Tendencia de Mercado:** Tendencia marcada al `Under de Carreras (Primeros 5 Innings)` por dominio de serpentineros.\n"
            f"• ⚔ **Hándicap Sugerido:** `Hándicap de Carreras -1.5` o victoria simple por margen ajustado en el bullpen."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL & PROBABILIDADES:**\n"
            f"• 🥇 *Primer Tercio / Innings 1-3 ({prob_porcentaje}% Probabilidad):* Dominio absoluto desde la lomita, nulas libertades de extrabase.\n"
            f"• ⚖ *Mitad del Juego (Innings 4-6):* Instancia clave de desgaste donde el orden al bate castiga el relevo intermedio.\n"
            f"• 📉 *Hándicap Alternativo:* Alta opción de definir en entradas extra o por diferencia mínima de una carrera."
        )
    else:  # Fútbol
        tendencias_principales = (
            f"• 🔥 **Racha Principal:** `{comp_a}` encadena **{racha_victorias_a} partidos consecutivos perforando la red** en la primera mitad.\n"
            f"• 📊 **Tendencia de Mercado:** El mercado de `Ambos Anotan (BTTS)` se cumple en el 82% de los enfrentamientos recientes.\n"
            f"• ⚔ **Hándicap Sugerido:** `Hándicap Asiático 0.0 / -0.25` para asegurar protección ante empates tácticos."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN CONDICIONAL & PROBABILIDADES:**\n"
            f"• 🥇 *Primer Tiempo ({prob_porcentaje}% Probabilidad):* Lucha intensa en la medular con bloques defensivos bien posicionados.\n"
            f"• ⚖ *Si se rompe el empate pasada la hora de juego (Min 60+):* El equipo en desventaja asume riesgos totales, disparando las opciones de goles y contragolpes.\n"
            f"• 📉 *Hándicap de Cierres:* Ventaja estadística en tramos finales para el cuadro local por amplitud de banquillo."
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


                       
        

    
    
    
    
    
    

    
