import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Diccionario temporal para guardar el estado de los usuarios
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("🏀 Analizar Baloncesto"), KeyboardButton("⚽ Analizar Fútbol"))
    
    bot.send_message(
        message.chat.id,
        "¡Bienvenido a tu Central Analítica Deportiva! 📊🔥\n\n"
        "Selecciona el deporte que deseas analizar:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text in ["🏀 Analizar Baloncesto", "⚽ Analizar Fútbol"])
def select_sport(message):
    sport = "Baloncesto" if "Baloncesto" in message.text else "Fútbol"
    user_data[message.chat.id] = {"sport": sport}
    
    bot.send_message(
        message.chat.id,
        f"Has seleccionado **{sport}**.\n\n"
        "Ahora, escribe el **partido o evento** (Ejemplo: *Lakers vs Celtics* o *Real Madrid vs Barcelona*):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_match_name)

def get_match_name(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {}
    
    user_data[chat_id]["match"] = message.text
    sport = user_data[chat_id].get("sport", "Deporte")
    
    if "Baloncesto" in sport:
        prompt = (
            "Excelente. Ahora envía los datos estadísticos separados por comas:\n"
            "**Asistencias, PorcentajeTL, Pérdidas**\n"
            "(Ejemplo: `5, 80, 2`)"
        )
    else:
        prompt = (
            "Excelente. Ahora envía los datos estadísticos separados por comas:\n"
            "**Remates al arco, Posesión(%), Tarjetas**\n"
            "(Ejemplo: `6, 55, 2`)"
        )

    bot.send_message(chat_id, prompt, parse_mode="Markdown")
    bot.register_next_step_handler(message, calculate_analytics)

def calculate_analytics(message):
    chat_id = message.chat.id
    try:
        # Limpiar y procesar los valores numéricos
        text = message.text.replace(" ", "")
        parts = text.split(",")
        
        if len(parts) != 3:
            raise ValueError("Formato inválido")
            
        val1 = float(parts[0])
        val2 = float(parts[1])
        val3 = float(parts[2])
        
        match_info = user_data.get(chat_id, {}).get("match", "Partido General")
        sport = user_data.get(chat_id, {}).get("sport", "Deporte")
        
        # Cálculo analítico estimado (Valor esperado / índice de rendimiento)
        estimated_value = round((val1 * 1.2) + (val2 * 0.05) - (val3 * 1.5), 2)
        
        report = (
            f"🎯 **Reporte de Análisis Deportivo**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"📌 **Categoría:** {sport}\n\n"
            f"📊 **Métricas Evaluadas:**\n"
            f"• Métrica 1: `{val1}`\n"
            f"• Métrica 2: `{val2}`\n"
            f"• Métrica 3: `{val3}`\n\n"
            f"🔥 **Valor Estimado / +EV:** **{estimated_value}**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"Usa /start para realizar un nuevo análisis."
        )
        
        bot.send_message(chat_id, report, parse_mode="Markdown")
        
    except Exception as e:
        bot.send_message(
            chat_id,
            "⚠️ Formato incorrecto o datos inválidos. Asegúrate de enviar exactamente 3 números separados por comas (Ejemplo: `5, 80, 2`).\n\nVuelve a intentarlo o escribe /start para reiniciar."
        )

# Mantener el bot parándose y escuchando de forma continua
if __name__ == "__main__":
    print("Bot iniciado correctamente...")
    bot.infinity_polling()
        
      
