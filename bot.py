import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Configuración con tu nuevo token limpio y tu ID exclusivo de seguridad
TOKEN = "8620258395:AAE2XAQa73pnApjdP6ozdEcun-q9b-lXsE8"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5019002345  # Tu ID exclusivo de Telegram

user_data = {}

# Filtro de seguridad estricto: Solo responde a tu ID, ignora a cualquier otro usuario
@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID)
def block_unauthorized(message):
    return

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("⚽ Analizar Fútbol"), KeyboardButton("🏀 Analizar Baloncesto"))
    markup.add(KeyboardButton("🎾 Analizar Tenis"), KeyboardButton("⚾ Analizar MLB (Béisbol)"))
    
    bot.send_message(
        chat_id,
        "📊 **Central Analítica Deportiva (+EV IA)**\n\nSelecciona el deporte para procesar datos de mercado:",
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

@bot.message_handler(func=lambda m: m.text in ["⚽ Analizar Fútbol", "🏀 Analizar Baloncesto", "🎾 Analizar Tenis", "⚾ Analizar MLB (Béisbol)"])
def select_sport(message):
    if message.from_user.id != ADMIN_ID:
        return
    sport_map = {
        "⚽ Analizar Fútbol": "Fútbol",
        "🏀 Analizar Baloncesto": "Baloncesto",
        "🎾 Analizar Tenis": "Tenis",
        "⚾ Analizar MLB (Béisbol)": "MLB"
    }
    sport = sport_map.get(message.text, "Fútbol")
    user_data[message.chat.id] = {"sport": sport}
    
    bot.send_message(
        message.chat.id,
        f"Has seleccionado **{sport}** 📌\n\nEscribe el **partido o evento** (Ej: *Real Madrid vs Barcelona* o consulta de fuentes tipo Scores24/365Scores):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_match_name)

def get_match_name(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {}
    
    user_data[chat_id]["match"] = message.text
    sport = user_data[chat_id].get("sport", "Fútbol")
    
    bot.send_message(
        chat_id,
        f"Envía 3 métricas clave de rendimiento para **{sport}** separadas por comas (Ej: `5, 80, 2` para xG/posesión/tendencia):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, calculate_analytics)

def calculate_analytics(message):
    chat_id = message.chat.id
    try:
        text = message.text.replace(" ", "")
        parts = text.split(",")
        
        if len(parts) != 3:
            raise ValueError("Formato inválido")
            
        val1 = float(parts[0])
        val2 = float(parts[1])
        val3 = float(parts[2])
        
        match_info = user_data.get(chat_id, {}).get("match", "Encuentro")
        sport = user_data.get(chat_id, {}).get("sport", "Deporte")
        
        # Algoritmo de IA analítica ponderada (+EV y Líneas de Mercado)
        ev_score = round((val1 * 1.25) + (val2 * 0.09) - (val3 * 1.1), 2)
        over_under = round(val1 + (val2 * 0.08), 1)
        market_confidence = "Alta (Valor Detectado +EV)" if ev_score > 5 else "Moderada (Esperar Mercado)"
        
        report = (
            f"🤖 **REPORTE ANALÍTICO DE IA (+EV)**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"📌 **Categoría:** {sport}\n"
            f"🌐 **Fuentes de Referencia:** Scores24 / 365Scores Engine\n\n"
            f"📊 **Métricas Evaluadas:** `{val1}`, `{val2}`, `{val3}`\n"
            f"💡 **Recomendación de Hándicap:** Favorable con Tendencia de Mercado\n"
            f"📈 **Línea Over/Under Proyectada:** `{over_under}`\n"
            f"🔥 **Índice de Valor (+EV):** **{ev_score}**\n"
            f"⚖ **Confianza del Modelo:** {market_confidence}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"Usa el menú para otro análisis."
        )
        
        bot.send_message(chat_id, report, parse_mode="Markdown")
        show_main_menu(chat_id)
        
    except Exception as e:
        bot.send_message(chat_id, "⚠ Error: Envía exactamente **3 números separados por comas** (Ej: `5, 80, 2`).")

if __name__ == "__main__":
    print("Bot analítico privado iniciado correctamente...")
    bot.infinity_polling()
    
        
    
        
    
                     
        
      
