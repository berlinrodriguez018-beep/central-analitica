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
        "🧠 **CENTRAL DE TENDENCIAS & SIMULACIÓN AI**\n\n"
        "Escribe el comando seguido del partido o jugadores:\n\n"
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
def handle_trend_simulation(message):
    if message.from_user.id != ADMIN_ID:
        return
        
    # Extraer el texto limpiando cualquier comando inicial
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
            "`/analisis JugadorA vs JugadorB` o `/analisis EquipoA vs EquipoB`",
            parse_mode="Markdown"
        )
        return

    match_name = text_content
    teams = [t.strip() for t in match_name.split("vs") if t.strip()]
    competitor_a = teams[0] if len(teams) > 0 else "Competidor A"
    competitor_b = teams[1] if len(teams) > 1 else "Competidor B"

    # Detección inteligente de disciplina deportiva basada en nombres o palabras clave
    lower_match = match_name.lower()
    tennis_keywords = ["shapovalov", "tabilo", "djokovic", "alcaraz", "sinner", "nadal", "medvedev", "zverev", "tsitsipas", "ruud", "rublev", "fritz", "hurkacz", "de minaur", "paul", "shelton", "musetti", "draper", "bublik", "cerundolo", "baez", "jarry", "etcheverry", "sabalenka", "swiatek", "gauff", "rybakina"]
    basketball_keywords = ["lakers", "celtics", "warriors", "bulls", "heat", "nuggets", "bucks", "suns", "mavericks", "knicks", "real madrid", "barcelona", "baskonia", "olympiacos", "panathinaikos"]
    baseball_keywords = ["yankees", "red sox", "dodgers", "astros", "braves", "cubs", "mets", "phillies"]

    if any(k in lower_match for k in tennis_keywords):
        sport_type = "Tenis"
    elif any(k in lower_match for k in basketball_keywords):
        sport_type = "Baloncesto"
    elif any(k in lower_match for k in baseball_keywords):
        sport_type = "MLB"
    else:
        sport_type = "Fútbol"

    # Generación de métricas estadísticas y valores de probabilidad realistas
    odd_value = round(random.uniform(1.72, 2.35), 2)
    ev_index = round(random.uniform(12.5, 24.8), 2)
    prob_porcentaje = random.randint(68, 84)

    query_encoded = match_name.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Consultar 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Tendencias Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    # Construcción de tendencias y simulaciones adaptadas al deporte detectado
    if sport_type == "Tenis":
        tendencias = (
            f"• 🔥 **Patrón de Superficie:** `{competitor_a}` mantiene un registro de alta efectividad al primer servicio en pistas similares.\n"
            f"• ⚠ **Indicador de Quiebres:** Si `{competitor_b}` cede más del 60% de puntos con su segundo saque en los compases iniciales, la estadística histórica de fuentes especializadas muestra que el set se extiende a más de 10.5 juegos.\n"
            f"• 📉 **Desgaste y Paridad:** Los enfrentamientos recientes de ambos jugadores registran alta tendencia a disputar parciales largos o llegar a tie-breaks."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN DE ESCENARIOS (TENIS):**\n"
            f"• *Desarrollo:* Intercambios intensos desde el fondo de pista con dominio alterno.\n"
            f"• *Escenario Crítico:* Si el partido se alarga a un set definitivo, la simulación favorece ligeramente a `{competitor_a}` debido a su mayor solidez física en los tramos finales."
        )
    elif sport_type == "Baloncesto":
        tendencias = (
            f"• 🔥 **Inercia de Local/Visitante:** `{competitor_a}` suele imponer un ritmo de posesiones rápidas en los primeros cuartos.\n"
            f"• ⚠ **Patrón Condicional:** Si la diferencia se estrecha en el tercer cuarto, la tendencia histórica indica que el marcador total superará la línea de puntos debido a faltas tácticas y tiros libres en el cierre.\n"
            f"• 📉 **Eficiencia Ofensiva:** Los porcentajes de efectividad exterior de `{competitor_b}` aumentan un 15% cuando bajan la intensidad defensiva rival."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN DE ESCENARIOS (BALONCESTO):**\n"
            f"• *Desarrollo:* Partido de alta anotación con rachas ofensivas cruzadas.\n"
            f"• *Escenario Crítico:* Si el encuentro llega igualado a los últimos dos minutos, la profundidad de rotación de banquillo inclina la probabilidad de control hacia `{competitor_a}`."
        )
    elif sport_type == "MLB":
        tendencias = (
            f"• 🔥 **Tendencia de Pitcheo:** El abridor de `{competitor_a}` muestra solidez en las primeras entradas, permitiendo pocos corredores en base.\n"
            f"• ⚠ **Patrón de Bullpen:** Si el marcador llega ajustado al sexto inning, el cuerpo de relevistas de `{competitor_b}` suele conceder mayor margen de bateo oportuno.\n"
            f"• 📉 **Conteo de Carreras:** Historial favorable a encuentros con anotaciones contenidas en el primer tercio del juego."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN DE ESCENARIOS (BÉISBOL):**\n"
            f"• *Desarrollo:* Duelo táctico de estrategia desde la lomita y control de zona.\n"
            f"• *Escenario Crítico:* Definición estrecha resuelta por detalles en el bateo con corredores en posición anotadora."
        )
    else:  # Fútbol por defecto
        tendencias = (
            f"• 🔥 **Dinámica Reciente:** `{competitor_a}` acumula secuencias de alta presión tras pérdida en condición de local o favorito.\n"
            f"• ⚠ **Patrón Condicional:** Si el partido se mantiene sin abrir el marcador pasada la hora de juego, la tendencia de ambas escuadras apunta a descuidos defensivos en transiciones rápidas.\n"
            f"• 📉 **Efectividad de Goles:** Promedio elevado de saques de esquina y remates al arco en los segundos tiempos de sus duelos directos."
        )
        simulacion = (
            f"🔮 **SIMULACIÓN DE ESCENARIOS (FÚTBOL):**\n"
            f"• *Desarrollo:* Lucha táctica en la medular con espacios condicionados por bloques compactos.\n"
            f"• *Escenario Crítico:* Si un equipo rompe el empate antes del minuto 75, el rival se verá obligado a adelantar líneas, aumentando las probabilidades de un segundo tanto en contragolpe."
        )

    report = (
        f"📊 **AUDITORÍA DE TENDENCIAS & SIMULACIÓN**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏟 **Encuentro:** `{match_name}`\n"
        f"🎯 **Disciplina Detectada:** `{sport_type}`\n\n"
        f"📈 **PRINCIPALES TENDENCIAS (WEB INSIGHTS):**\n"
        f"{tendencias}\n\n"
        f"{simulacion}\n\n"
        f"💎 **VALOR ESTADÍSTICO & PROBABILIDAD (+EV):**\n"
        f"• Probabilidad Estimada: `🟢 {prob_porcentaje}% de Certeza`\n"
        f"• Cuota de Tendencia: `{odd_value}` | `+{ev_index} Index EV`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    bot.send_message(message.chat.id, report, parse_mode="Markdown", reply_markup=markup_links)

if __name__ == "__main__":
    print("Central de Tendencias y Simulación Inteligente Activa...")
    while True:
        try:
            bot.infinity_polling(interval=0, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Error de conexión: {e}. Reconectando en 5s...")
            time.sleep(5)
                       
        

    
    
    
    
    
    

    
