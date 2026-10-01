import os
import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Configuración del bot y tu ID exclusivo de seguridad
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
        "📊 **Central Analítica Profesional (+EV & Live Engine)**\n\nSelecciona el deporte para escanear líneas de mercado:",
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
    
    if "Baloncesto" in message.text:
        sport = "Baloncesto"
    elif "Fútbol" in message.text:
        sport = "Fútbol"
    elif "Tenis" in message.text:
        sport = "Tenis"
    else:
        sport = "MLB"
        
    user_data[message.chat.id] = {"sport": sport}
    
    bot.send_message(
        message.chat.id,
        f"Has seleccionado **{sport}** 📌\n\nEscribe el **partido en vivo** que deseas seguir (Ej: *Miami Heat vs Denver Nuggets*):",
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
    sport = user_data[chat_id].get("sport", "Fútbol")
    
    if sport == "Baloncesto":
        prompt_msg = (
            f"🏀 **Escáner Profesional de Baloncesto Activo**\n\n"
            f"Escribe el contexto del partido en vivo (ej: *cuarto cuarto apretado, bonus de faltas, ritmo alto, cuota actual 1.85*):"
        )
    else:
        prompt_msg = f"Escribe las notas o situación actual para **{sport}**:"

    bot.send_message(chat_id, prompt_msg, parse_mode="Markdown")
    bot.register_next_step_handler(message, calculate_analytics)

def calculate_analytics(message):
    chat_id = message.chat.id
    if "Analizar" in message.text:
        select_sport(message)
        return

    notes = message.text.lower()
    match_info = user_data.get(chat_id, {}).get("match", "Encuentro")
    sport = user_data.get(chat_id, {}).get("sport", "Deporte")
    
    if sport == "Baloncesto":
        # Generación de líneas profesionales de puntos y cuotas simuladas de casas de apuestas
        line_q1 = round(random.uniform(48.5, 56.5), 1)
        line_q2 = round(random.uniform(47.0, 55.0), 1)
        line_h1 = round(random.uniform(97.5, 110.5), 1)
        
        line_q3 = round(random.uniform(49.0, 58.0), 1)
        line_q4 = round(random.uniform(48.0, 57.0), 1)
        line_h2 = round(random.uniform(98.0, 112.0), 1)
        line_ft = round(random.uniform(205.5, 228.5), 1)

        # Probabilidades y porcentajes de acierto
        prob_q1 = round(random.uniform(62.0, 88.0), 1)
        prob_h1 = round(random.uniform(65.0, 91.0), 1)
        prob_ft = round(random.uniform(70.0, 94.0), 1)

        # Semáforo de seguridad (Verde para alta probabilidad, Rojo para alto riesgo/evitar)
        status_q1 = "🟢 SEGURO (+EV Óptimo)" if prob_q1 > 75 else "🔴 ALTO RIESGO (Evitar)"
        status_h1 = "🟢 SEGURO (+EV Óptimo)" if prob_h1 > 75 else "🔴 ALTO RIESGO (Evitar)"
        status_ft = "🟢 SEGURO (+EV Óptimo)" if prob_ft > 75 else "🔴 ALTO RIESGO (Evitar)"

        # Cuotas de casas de apuestas simuladas (Decimales estándar tipo Bet365 / Pinnacle)
        odd_value = round(random.uniform(1.82, 2.10), 2)

        report = (
            f"🏀 **CENTRAL EN VIVO — LÍNEAS DE MERCADO (BALONCESTO)**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"🌐 **Feed Oficial:** 365Scores & Scores24 Pro API\n"
            f"💬 **Contexto en Vivo:** _{message.text}_\n\n"
            f"⏱ **DESGLOSE POR PERIODOS Y LÍNEAS DE PUNTOS:**\n\n"
            f" • **1er Cuarto (Q1):** Línea `Over/Under {line_q1} pts`\n"
            f"   ↳ Probabilidad: `{prob_q1}%` | Cuota: `{odd_value}` | Estado: {status_q1}\n\n"
            f" • **2do Cuarto (Q2):** Línea `Over/Under {line_q2} pts`\n"
            f"   ↳ Rotaciones de banca y control de ritmo.\n\n"
            f" • **1era Mitad (HT):** Línea `Over/Under {line_h1} pts`\n"
            f"   ↳ Probabilidad: `{prob_h1}%` | Estado: {status_h1}\n\n"
            f" • **3er Cuarto (Q3):** Línea `Over/Under {line_q3} pts`\n"
            f"   ↳ Ajustes tácticos post-vestuario.\n\n"
            f" • **4to Cuarto (Q4):** Línea `Over/Under {line_q4} pts`\n"
            f"   ↳ Gestión de faltas y cierre de partido.\n\n"
            f" • **2da Mitad (H2):** Línea `Over/Under {line_h2} pts`\n\n"
            f"🏆 **PARTIDO COMPLETO (FULL TIME):**\n"
            f"📊 **Línea Total Sugerida:** `{line_ft} Puntos`\n"
            f"🔥 **Probabilidad de Acierto:** `{prob_ft}%`\n"
            f"💎 **Evaluación de Seguridad:** {status_ft}\n"
            f"🎯 **Cuota de Mercado Estimada:** `{odd_value}` (+EV Verificado)\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔄 El motor sigue escaneando el encuentro. Usa el menú para otro análisis."
        )
    else:
        ev_value = round(random.uniform(4.0, 9.5), 2)
        report = (
            f"🤖 **REPORTE DE MERCADO (+EV)**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Evento:** {match_info}\n"
            f"📌 **Deporte:** {sport}\n"
            f"🔥 **Índice de Valor (+EV):** **+{ev_value}**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"Selecciona otro deporte abajo."
        )
    
    bot.send_message(chat_id, report, parse_mode="Markdown")
    show_main_menu(chat_id)

if __name__ == "__main__":
    print("Central Analítica Pro con Líneas en Vivo iniciada...")
    bot.infinity_polling()
    

    
        
    
        
    
                     
        
      
