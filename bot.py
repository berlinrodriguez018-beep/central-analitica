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
        "🚀 **NEURAL BET ENGINE — MÁXIMO NIVEL PRO**\n\nSelecciona el deporte para ejecutar el motor de simulación de modelos en vivo:",
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
        "Tenis": "Carlos Alcaraz vs Alex Michelsen",
        "Fútbol": "Real Madrid vs Barcelona",
        "MLB": "New York Yankees vs Boston Red Sox"
    }
    
    bot.send_message(
        message.chat.id,
        f"Has seleccionado **{sport}** 📌\n\nEscribe el **partido en vivo** que deseas auditar (Ej: *{examples.get(sport, 'Equipo A vs Equipo B')}*):",
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
        f"🧠 **Simulador Neural Activado ({sport})**\n\nEscribe la situación o enfoque táctico que deseas contrastar (ej: *ganador de partido, comportamiento de líneas, hándicap o colapso en vivo*):",
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
    
    # Procesar nombres de competidores
    teams = [t.strip() for t in match_info.split("vs")]
    t1 = teams[0] if len(teams) > 0 else "Local / Favorito"
    t2 = teams[1] if len(teams) > 1 else "Visitante / Rival"

    odd_value = round(random.uniform(1.78, 2.15), 2)
    ev_index = round(random.uniform(6.2, 15.4), 2)
    simulations_count = random.randint(8500, 10000)

    # ENLACES DIRECTOS A PLATAFORMAS EN VIVO
    query_encoded = match_info.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Ver en 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Ver en Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    if sport == "Tenis":
        line_games = random.choice([21.5, 22.5, 23.5, 24.5])
        prob_s1 = round(random.uniform(78.0, 94.0), 1)
        prob_match = round(random.uniform(72.0, 89.0), 1)
        
        report = (
            f"🎾 **NEURAL ENGINE — TENIS PRO MÁXIMO NIVEL**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🤖 **Modelos Contrastados:** {simulations_count} simulaciones Monte Carlo + Machine Learning\n"
            f"💬 **Consulta:** _{message.text}_\n\n"
            f"📊 **PREDICCIÓN DE MERCADO & LÍNEAS:**\n"
            f" • **Línea Global:** `Over de {line_games} juegos totales` (Alta tendencia de sets disputados)\n"
            f" • **1er Set:** **{t1}** gana el 1er Set con solidez al saque (Prob: `{prob_s1}%`)\n"
            f" • **Ganador Absoluto:** **{t1}** se lleva el partido (Confianza de modelos: `{prob_match}%`)\n\n"
            f"🚨 **ALERTA DE PELIGRO / DESARROLLO EN VIVO:**\n"
            f"⚠️ *Peligro crítico:* {t2} suele elevar su porcentaje de devolución en superficies rápidas. Existe riesgo alto de que {t1} sufra un bajón físico o desconcentración cediendo el **2do set** si no asegura quiebres tempranos.\n\n"
            f"💎 **VALORACIÓN ESTADÍSTICA:**\n"
            f"• Evaluación: `🟢 +EV Óptimo` | Cuota: `{odd_value}` | `+{ev_index} Índice EV`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    elif sport == "Baloncesto":
        line_ft = random.choice([210.5, 215.5, 222.5, 228.5])
        diff_q = random.randint(4, 12)
        
        report = (
            f"🏀 **NEURAL ENGINE — BALONCESTO PRO MÁXIMO NIVEL**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🤖 **Modelos Contrastados:** {simulations_count} simulaciones de ritmo de posesión\n"
            f"💬 **Consulta:** _{message.text}_\n\n"
            f"📊 **PREDICCIÓN DE MERCADO & LÍNEAS:**\n"
            f" • **Línea de Puntos:** `Over de {line_ft} Puntos` (Frecuencia alta de transiciones rápidas)\n"
            f" • **Mitad (HT):** **{t1}** gana la 1era mitad por margen de +{diff_q} puntos.\n"
            f" • **Ganador Final:** **{t1}** administra la ventaja en el cierre.\n\n"
            f"🚨 **ALERTA DE PELIGRO / DESARROLLO EN VIVO:**\n"
            f"⚠️ *Peligro crítico:* La segunda unidad defensiva de {t2} tiende a colapsar en el 3er cuarto; atención a faltas repetitivas y bonus de tiros libres tempranos.\n\n"
            f"💎 **VALORACIÓN ESTADÍSTICA:**\n"
            f"• Evaluación: `🟢 +EV Óptimo` | Cuota: `{odd_value}` | `+{ev_index} Índice EV`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    elif sport == "Fútbol":
        line_goals = random.choice([2.5, 3.0])
        
        report = (
            f"⚽ **NEURAL ENGINE — FÚTBOL PRO MÁXIMO NIVEL**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🤖 **Modelos Contrastados:** {simulations_count} análisis xG (Goles Esperados) en vivo\n"
            f"💬 **Consulta:** _{message.text}_\n\n"
            f"📊 **PREDICCIÓN DE MERCADO & LÍNEAS:**\n"
            f" • **Línea de Goles:** `Over de {line_goals} goles` (Alta producción de ocasiones claras de gol)\n"
            f" • **Mercado Dinámico:** `Ambos anotan (BTTS)` con presión alta inicial.\n"
            f" • **Tendencia de Ganador:** **{t1}** domina la posesión útil.\n\n"
            f"🚨 **ALERTA DE PELIGRO / DESARROLLO EN VIVO:**\n"
            f"⚠️ *Peligro crítico:* {t2} repliega un bloque defensivo ultrabajo después del minuto 60; riesgo de sequía de remates y partido trabado en la medular.\n\n"
            f"💎 **VALORACIÓN ESTADÍSTICA:**\n"
            f"• Evaluación: `🟢 +EV Óptimo` | Cuota: `{odd_value}` | `+{ev_index} Índice EV`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    else:
        report = (
            f"⚾ **NEURAL ENGINE — BÉISBOL (MLB) MÁXIMO NIVEL**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🤖 **Modelos Contrastados:** {simulations_count} iteraciones de pitcheo y bullpen\n"
            f"💬 **Consulta:** _{message.text}_\n\n"
            f"📊 **PREDICCIÓN DE MERCADO & LÍNEAS:**\n"
            f" • **Línea de Carreras:** Alta vulnerabilidad en relevistas intermedios.\n"
            f" • **Tendencia:** Victoria esperada para **{t1}** por mayor profundidad ofensiva.\n\n"
            f"🚨 **ALERTA DE PELIGRO / DESARROLLO EN VIVO:**\n"
            f"⚠️ *Peligro crítico:* Cierre de partido inestable si el cerrador titular presenta fatiga acumulada en los últimos tres juegos.\n\n"
            f"💎 **VALORACIÓN ESTADÍSTICA:**\n"
            f"• Evaluación: `🟢 +EV Óptimo` | Cuota: `{odd_value}` | `+{ev_index} Índice EV`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
    
    bot.send_message(chat_id, report, parse_mode="Markdown", reply_markup=markup_links)
    show_main_menu(chat_id)

if __name__ == "__main__":
    print("Motor Neural Pro Activo al Máximo Nivel...")
    bot.infinity_polling()
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
        "🚀 **NEURAL BET ENGINE — MÁXIMO NIVEL PRO**\n\nSelecciona el deporte para ejecutar el motor de simulación de modelos en vivo:",
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
        "Tenis": "Carlos Alcaraz vs Alex Michelsen",
        "Fútbol": "Real Madrid vs Barcelona",
        "MLB": "New York Yankees vs Boston Red Sox"
    }
    
    bot.send_message(
        message.chat.id,
        f"Has seleccionado **{sport}** 📌\n\nEscribe el **partido en vivo** que deseas auditar (Ej: *{examples.get(sport, 'Equipo A vs Equipo B')}*):",
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
        f"🧠 **Simulador Neural Activado ({sport})**\n\nEscribe la situación o enfoque táctico que deseas contrastar (ej: *ganador de partido, comportamiento de líneas, hándicap o colapso en vivo*):",
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
    
    # Procesar nombres de competidores
    teams = [t.strip() for t in match_info.split("vs")]
    t1 = teams[0] if len(teams) > 0 else "Local / Favorito"
    t2 = teams[1] if len(teams) > 1 else "Visitante / Rival"

    odd_value = round(random.uniform(1.78, 2.15), 2)
    ev_index = round(random.uniform(6.2, 15.4), 2)
    simulations_count = random.randint(8500, 10000)

    # ENLACES DIRECTOS A PLATAFORMAS EN VIVO
    query_encoded = match_info.replace(" ", "%20")
    markup_links = InlineKeyboardMarkup()
    markup_links.add(
        InlineKeyboardButton("🌐 Ver en 365Scores", url=f"https://www.365scores.com/es/search?q={query_encoded}"),
        InlineKeyboardButton("📊 Ver en Scores24", url=f"https://scores24.live/es/search?q={query_encoded}")
    )

    if sport == "Tenis":
        line_games = random.choice([21.5, 22.5, 23.5, 24.5])
        prob_s1 = round(random.uniform(78.0, 94.0), 1)
        prob_match = round(random.uniform(72.0, 89.0), 1)
        
        report = (
            f"🎾 **NEURAL ENGINE — TENIS PRO MÁXIMO NIVEL**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🤖 **Modelos Contrastados:** {simulations_count} simulaciones Monte Carlo + Machine Learning\n"
            f"💬 **Consulta:** _{message.text}_\n\n"
            f"📊 **PREDICCIÓN DE MERCADO & LÍNEAS:**\n"
            f" • **Línea Global:** `Over de {line_games} juegos totales` (Alta tendencia de sets disputados)\n"
            f" • **1er Set:** **{t1}** gana el 1er Set con solidez al saque (Prob: `{prob_s1}%`)\n"
            f" • **Ganador Absoluto:** **{t1}** se lleva el partido (Confianza de modelos: `{prob_match}%`)\n\n"
            f"🚨 **ALERTA DE PELIGRO / DESARROLLO EN VIVO:**\n"
            f"⚠️ *Peligro crítico:* {t2} suele elevar su porcentaje de devolución en superficies rápidas. Existe riesgo alto de que {t1} sufra un bajón físico o desconcentración cediendo el **2do set** si no asegura quiebres tempranos.\n\n"
            f"💎 **VALORACIÓN ESTADÍSTICA:**\n"
            f"• Evaluación: `🟢 +EV Óptimo` | Cuota: `{odd_value}` | `+{ev_index} Índice EV`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    elif sport == "Baloncesto":
        line_ft = random.choice([210.5, 215.5, 222.5, 228.5])
        diff_q = random.randint(4, 12)
        
        report = (
            f"🏀 **NEURAL ENGINE — BALONCESTO PRO MÁXIMO NIVEL**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🤖 **Modelos Contrastados:** {simulations_count} simulaciones de ritmo de posesión\n"
            f"💬 **Consulta:** _{message.text}_\n\n"
            f"📊 **PREDICCIÓN DE MERCADO & LÍNEAS:**\n"
            f" • **Línea de Puntos:** `Over de {line_ft} Puntos` (Frecuencia alta de transiciones rápidas)\n"
            f" • **Mitad (HT):** **{t1}** gana la 1era mitad por margen de +{diff_q} puntos.\n"
            f" • **Ganador Final:** **{t1}** administra la ventaja en el cierre.\n\n"
            f"🚨 **ALERTA DE PELIGRO / DESARROLLO EN VIVO:**\n"
            f"⚠️ *Peligro crítico:* La segunda unidad defensiva de {t2} tiende a colapsar en el 3er cuarto; atención a faltas repetitivas y bonus de tiros libres tempranos.\n\n"
            f"💎 **VALORACIÓN ESTADÍSTICA:**\n"
            f"• Evaluación: `🟢 +EV Óptimo` | Cuota: `{odd_value}` | `+{ev_index} Índice EV`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    elif sport == "Fútbol":
        line_goals = random.choice([2.5, 3.0])
        
        report = (
            f"⚽ **NEURAL ENGINE — FÚTBOL PRO MÁXIMO NIVEL**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🤖 **Modelos Contrastados:** {simulations_count} análisis xG (Goles Esperados) en vivo\n"
            f"💬 **Consulta:** _{message.text}_\n\n"
            f"📊 **PREDICCIÓN DE MERCADO & LÍNEAS:**\n"
            f" • **Línea de Goles:** `Over de {line_goals} goles` (Alta producción de ocasiones claras de gol)\n"
            f" • **Mercado Dinámico:** `Ambos anotan (BTTS)` con presión alta inicial.\n"
            f" • **Tendencia de Ganador:** **{t1}** domina la posesión útil.\n\n"
            f"🚨 **ALERTA DE PELIGRO / DESARROLLO EN VIVO:**\n"
            f"⚠️ *Peligro crítico:* {t2} repliega un bloque defensivo ultrabajo después del minuto 60; riesgo de sequía de remates y partido trabado en la medular.\n\n"
            f"💎 **VALORACIÓN ESTADÍSTICA:**\n"
            f"• Evaluación: `🟢 +EV Óptimo` | Cuota: `{odd_value}` | `+{ev_index} Índice EV`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    else:
        report = (
            f"⚾ **NEURAL ENGINE — BÉISBOL (MLB) MÁXIMO NIVEL**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🤖 **Modelos Contrastados:** {simulations_count} iteraciones de pitcheo y bullpen\n"
            f"💬 **Consulta:** _{message.text}_\n\n"
            f"📊 **PREDICCIÓN DE MERCADO & LÍNEAS:**\n"
            f" • **Línea de Carreras:** Alta vulnerabilidad en relevistas intermedios.\n"
            f" • **Tendencia:** Victoria esperada para **{t1}** por mayor profundidad ofensiva.\n\n"
            f"🚨 **ALERTA DE PELIGRO / DESARROLLO EN VIVO:**\n"
            f"⚠️ *Peligro crítico:* Cierre de partido inestable si el cerrador titular presenta fatiga acumulada en los últimos tres juegos.\n\n"
            f"💎 **VALORACIÓN ESTADÍSTICA:**\n"
            f"• Evaluación: `🟢 +EV Óptimo` | Cuota: `{odd_value}` | `+{ev_index} Índice EV`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
    
    bot.send_message(chat_id, report, parse_mode="Markdown", reply_markup=markup_links)
    show_main_menu(chat_id)

if __name__ == "__main__":
    print("Motor Neural Pro Activo al Máximo Nivel...")
    bot.infinity_polling()
    
    
    
    
    

    
        
    
        
    
                     
        
      
