import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Memoria temporal para rastrear el flujo de cada usuario
user_data = {}

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(
        KeyboardButton("⚽ Analizar Fútbol"), 
        KeyboardButton("🏀 Analizar Baloncesto")
    )
    markup.add(
        KeyboardButton("🎾 Analizar Tenis"), 
        KeyboardButton("⚾ Analizar MLB (Béisbol)")
    )
    
    bot.send_message(
        chat_id,
        "📊 **Central Analítica Deportiva - Menú Principal**\n\n"
        "Selecciona el deporte que deseas analizar usando los botones inferiores:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text and message.text.lower() in ["hola", "empezar", "inicio", "bot", "menu"]):
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text in [
    "⚽ Analizar Fútbol", 
    "🏀 Analizar Baloncesto", 
    "🎾 Analizar Tenis", 
    "⚾ Analizar MLB (Béisbol)"
])
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
        f"Has seleccionado **{sport}** 📌\n\n"
        "Ahora, escribe el **partido o evento** (Ejemplo: *Real Madrid vs Barcelona* o *Yankees vs Red Sox*):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_match_name)

def get_match_name(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {}
    
    user_data[chat_id]["match"] = message.text
    sport = user_data[chat_id].get("sport", "Fútbol")
    
    # Guías personalizadas de métricas avanzadas según el deporte
    prompts = {
        "Fútbol": (
            "⚽ **Fútbol (Pre-partido / En Vivo)**\n"
            "Envía 3 métricas clave separadas por comas:\n"
            "**Remates al arco, Posesión(%), Tarjetas/Corners**\n"
            "(Ejemplo: `6, 55, 4`)"
        ),
        "Baloncesto": (
            "🏀 **Baloncesto (NBA / Ligas)**\n"
            "Envía 3 métricas clave separadas por comas:\n"
            "**Eficiencia Ofensiva, Porcentaje Triples(%), Rebotes/Asistencias**\n"
            "(Ejemplo: `112, 38, 45`)"
        ),
        "Tenis": (
            "🎾 **Tenis (Sets / Jugadores)**\n"
            "Envía 3 métricas clave separadas por comas:\n"
            "**% Primer Servicio, Quiebres Salvados, Errores No Forzados**\n"
            "(Ejemplo: `68, 75, 18`)"
        ),
        "MLB": (
            "⚾ **MLB (Béisbol - Innings / Carreras)**\n"
            "Envía 3 métricas clave separadas por comas:\n"
            "**ERA del Picheo, Carreras Anotadas por Juego, OBP (Embasarse)**\n"
            "(Ejemplo: `3.40, 5.2, 0.330`)"
        )
    }

    prompt_text = prompts.get(sport, prompts["Fútbol"])
    bot.send_message(chat_id, prompt_text, parse_mode="Markdown")
    bot.register_next_step_handler(message, calculate_advanced_analytics)

def calculate_advanced_analytics(message):
    chat_id = message.chat.id
    try:
        text = message.text.replace(" ", "")
        parts = text.split(",")
        
        if len(parts) != 3:
            raise ValueError("Formato inválido")
            
        val1 = float(parts[0])
        val2 = float(parts[1])
        val3 = float(parts[2])
        
        match_info = user_data.get(chat_id, {}).get("match", "Encuentro Deportivo")
        sport = user_data.get(chat_id, {}).get("sport", "Deporte")
        
        # Algoritmo analítico ponderado para generar proyecciones de mercado (+EV)
        ev_score = round((val1 * 1.15) + (val2 * 0.08) - (val3 * 1.2), 2)
        over_under_proj = round(val1 + (val2 * 0.1), 1)
        
        # Generación de mercados analíticos automáticos
        if sport == "Fútbol":
            mercado_ganador = "Local / Gana o Empata (Doble Oportunidad)" if ev_score > 20 else "Visita / Alta de Goles"
            handicap_sugerido = "Hándicap Asiático: -0.5" if ev_score > 25 else "Hándicap Asiático: +1.0"
        elif sport == "Baloncesto":
            mercado_ganador = "Moneyline (Ganador del Partido): Favorito Local" if ev_score > 50 else "Moneyline: Visitante"
            handicap_sugerido = "Hándicap de Puntos: -4.5"
        elif sport == "Tenis":
            mercado_ganador = "Ganador del Partido & Ganador del 1er Set" if ev_score > 40 else "Total de Sets: Más de 2.5"
            handicap_sugerido = "Hándicap de Games: -2.5"
        else:  # MLB
            mercado_ganador = "Moneyline (Ganador del Inning / Partido)" if ev_score > 15 else "Visitor Run Line"
            handicap_sugerido = "Hándicap de Carreras (-1.5)"

        report = (
            f"🎯 **REPORTE ANALÍTICO PROFESIONAL (+EV)**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏟 **Encuentro:** {match_info}\n"
            f"📌 **Categoría:** {sport}\n\n"
            f"📊 **Métricas Evaluadas:**\n"
            f"• Factor Principal: `{val1}`\n"
            f"• Eficiencia / Porcentaje: `{val2}`\n"
            f"• Riesgo / Errores: `{val3}`\n\n"
            f"💡 **Proyecciones de Mercado:**\n"
            f"• **Apuesta Ganadora Principal:** {mercado_ganador}\n"
            f"• **Hándicap Óptimo:** {handicap_sugerido}\n"
            f"• **Proyección Over / Under:** `{over_under_proj}`\n"
            f"• **Índice de Valor (+EV):** **{ev_score}** 📈\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Selecciona otro deporte abajo para un nuevo análisis."
        )
        
        bot.send_message(chat_id, report, parse_mode="Markdown")
        show_main_menu(chat_id)
        
    except Exception as e:
        bot.send_message(
            chat_id,
            "⚠️ Error en el formato de los datos. Asegúrate de enviar exactamente **3 números separados por comas** (Ejemplo: `5, 80, 2`). Vuelve a intentar o usa el menú."
        )

if __name__ == "__main__":
    print("Central Analítica iniciada correctamente...")
    bot.infinity_polling()
                     
        
      
