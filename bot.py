import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

user_data = {}

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("⚽ Analizar Fútbol"), KeyboardButton("🏀 Analizar Baloncesto"))
    markup.add(KeyboardButton("🎾 Analizar Tenis"), KeyboardButton("⚾ Analizar MLB (Béisbol)"))
    
    bot.send_message(
        chat_id,
        "📊 **Central Analítica Deportiva**\n\nSelecciona el deporte que deseas analizar:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda m: m.text and m.text.lower() in ["hola", "empezar", "inicio", "bot", "menu"])
def greeting_handler(message):
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda m: m.text in ["⚽ Analizar Fútbol", "🏀 Analizar Baloncesto", "🎾 Analizar Tenis", "⚾ Analizar MLB (Béisbol)"])
def select_sport(message):
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
        f"Has seleccionado **{sport}** 📌\n\nEscribe el **partido o evento** (Ej: *Real Madrid vs Barcelona*):",
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
        f"Envía 3 métricas clave para **{sport}** separadas por comas (Ej: `5, 80, 2`):",
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
        
        ev_score = round((val1 * 1.15) + (val2 * 0.08) - (val3 * 1.2), 2)
        over_under = round(val1 + (val2 * 0.1), 1)
        
        report = (
            f"🎯 **REPORTE ANALÍTICO (+EV)**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"📌 **Categoría:** {sport}\n\n"
            f"📊 **Métricas:** `{val1}`, `{val2}`, `{val3}`\n"
            f"💡 **Predicción / Hándicap:** Favorable con Valor\n"
            f"📈 **Over/Under Proyectado:** `{over_under}`\n"
            f"🔥 **Índice +EV:** **{ev_score}**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"Usa el menú para otro análisis."
        )
        
        bot.send_message(chat_id, report, parse_mode="Markdown")
        show_main_menu(chat_id)
        
    except Exception as e:
        bot.send_message(chat_id, "⚠️️ Error: Envía exactamente **3 números separados por comas** (Ej: `5, 80, 2`).")

if __name__ == "__main__":
    print("Bot iniciado correctamente...")
    bot.infinity_polling()
    
                     
        
      
