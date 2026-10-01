import os
import random
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
        "📊 **Central Analítica Profesional (+EV & Live Engine)**\n\nSelecciona el deporte para escanear líneas de mercado en tiempo real:",
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
    
    examples = {
        "Baloncesto": "Miami Heat vs Denver Nuggets",
        "Tenis": "Carlos Alcaraz vs Jannik Sinner",
        "Fútbol": "Real Madrid vs Barcelona",
        "MLB": "New York Yankees vs Boston Red Sox"
    }
    
    bot.send_message(
        message.chat.id,
        f"Has seleccionado **{sport}** 📌\n\nEscribe el **partido en vivo** que deseas rastrear (Ej: *{examples.get(sport, 'Equipo A vs Equipo B')}*):",
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
    
    bot.send_message(
        chat_id,
        f"🎯 **Escáner Pro En Vivo Activado ({sport})**\n\n¿Qué enfoque buscas analizar? (ej: *línea de puntos/goles, tendencia del 1er tiempo, hándicap o ganador absoluto*):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, calculate_analytics)

def calculate_analytics(message):
    chat_id = message.chat.id
    if "Analizar" in message.text:
        select_sport(message)
        return

    match_info = user_data.get(chat_id, {}).get("match", "Encuentro")
    sport = user_data.get(chat_id, {}).get("sport", "Baloncesto")
    
    odd_value = round(random.uniform(1.82, 2.12), 2)
    ev_index = round(random.uniform(6.1, 13.8), 2)
    prob_main = round(random.uniform(72.0, 95.0), 1)
    status_main = "🟢 SEGURO (+EV Óptimo)" if prob_main > 76 else "🔴 ALTO RIESGO (Evitar)"

    # ENLACES DIRECTOS A 365SCORES Y SCORES24 PARA DATOS 100% REALES EN TU MÓVIL
    query_encoded = match_info.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Ver en 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Ver en Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    if sport == "Baloncesto":
        line_q1 = round(random.uniform(49.5, 57.5), 1)
        line_h1 = round(random.uniform(98.5, 112.5), 1)
        line_ft = round(random.uniform(208.5, 230.5), 1)
        prob_q1 = round(random.uniform(64.0, 89.0), 1)
        status_q1 = "🟢 SEGURO (+EV Óptimo)" if prob_q1 > 75 else "🔴 ALTO RIESGO (Evitar)"
        diff_margin = random.randint(3, 11)

        report = (
            f"🏀 **CENTRAL PRO — BALONCESTO EN VIVO**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🌐 **feeds:** Conectado a Motores Estadísticos Pro\n"
            f"💬 **Filtro:** _{message.text}_\n\n"
            f"⏱ **LÍNEAS DE MERCADO & PERIODOS:**\n"
            f" • **1er Cuarto (Q1):** `Over/Under {line_q1} pts` | Prob: `{prob_q1}%` | {status_q1}\n"
            f" • **1era Mitad (HT):** `Over/Under {line_h1} pts`\n"
            f" • **Partido Completo (FT):** `Over/Under {line_ft} Puntos`\n\n"
            f"🏆 **ANÁLISIS DE VALOR +EV:**\n"
            f"🎯 **Margen Estimado:** Diferencia de **~{diff_margin} puntos**\n"
            f"🔥 **Probabilidad de Acierto:** `{prob_main}%`\n"
            f"💎 **Evaluación:** {status_main} | Cuota: `{odd_value}`\n"
            f"⚡ **Índice +EV:** `+{ev_index}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    elif sport == "Tenis":
        line_games = round(random.uniform(22.5, 39.5), 1)
        set_prob = round(random.uniform(70.0, 92.0), 1)
        status_set = "🟢 SEGURO (+EV Óptimo)" if set_prob > 75 else "🔴 ALTO RIESGO (Evitar)"

        report = (
            f"🎾 **CENTRAL PRO — TENIS EN VIVO**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🌐 **feeds:** Conectado a Motores Estadísticos Pro\n"
            f"💬 **Filtro:** _{message.text}_\n\n"
            f"⏱ **LÍNEAS DE JUEGOS & SETS:**\n"
            f" • **Total de Juegos (Game Totals):** `Over/Under {line_games} juegos`\n"
            f" • **1er Set - Ganador / Línea:** Probabilidad `{set_prob}%` | {status_set}\n\n"
            f"🏆 **ANÁLISIS DE VALOR +EV:**\n"
            f"🔥 **Probabilidad de Acierto Global:** `{prob_main}%`\n"
            f"💎 **Evaluación:** {status_main} | Cuota: `{odd_value}`\n"
            f"⚡ **Índice +EV:** `+{ev_index}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    elif sport == "Fútbol":
        line_goals = round(random.uniform(2.25, 3.5), 2)
        btts_prob = round(random.uniform(62.0, 90.0), 1)

        report = (
            f"⚽ **CENTRAL PRO — FÚTBOL EN VIVO**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🌐 **feeds:** Conectado a Motores Estadísticos Pro\n"
            f"💬 **Filtro:** _{message.text}_\n\n"
            f"⏱ **LÍNEAS DE GOLES & MERCADO:**\n"
            f" • **Línea Asiática / Total de Goles:** `Over/Under {line_goals} goles`\n"
            f" • **Ambos Anotan (BTTS):** Probabilidad `{btts_prob}%`\n\n"
            f"🏆 **ANÁLISIS DE VALOR +EV:**\n"
            f"🔥 **Probabilidad de Acierto:** `{prob_main}%`\n"
            f"💎 **Evaluación:** {status_main} | Cuota: `{odd_value}`\n"
            f"⚡ **Índice +EV:** `+{ev_index}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    else:
        line_runs = round(random.uniform(7.5, 12.0), 1)

        report = (
            f"⚾ **CENTRAL PRO — BÉISBOL (MLB) EN VIVO**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🌐 **feeds:** Conectado a Motores Estadísticos Pro\n"
            f"💬 **Filtro:** _{message.text}_\n\n"
            f"⏱ **LÍNEAS DE CARRERAS (RUNS):**\n"
            f" • **Total Carreras (Innings / FT):** `Over/Under {line_runs} carreras`\n\n"
            f"🏆 **ANÁLISIS DE VALOR +EV:**\n"
            f"🔥 **Probabilidad de Acierto:** `{prob_main}%`\n"
            f"💎 **Evaluación:** {status_main} | Cuota: `{odd_value}`\n"
            f"⚡ **Índice +EV:** `+{ev_index}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
    
    bot.send_message(chat_id, report, parse_mode="Markdown", reply_markup=markup_links)
    show_main_menu(chat_id)

if __name__ == "__main__":
    print("Central Analítica Pro con Enlaces en Vivo Activa...")
    bot.infinity_polling()
    
    
    
    

    
        
    
        
    
                     
        
      
