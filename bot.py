import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Configurar logs básicos
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Bienvenido a tu Central Analítica! 🏀📊\n\n"
        "Envía los datos estadísticos en este formato:\n"
        "Asistencias, PorcentajeTL, Pérdidas\n\n"
        "Ejemplo: 5, 80, 2"
    )

async def calcular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    try:
        # Separa los valores por comas
        partes = [float(x.strip()) for x in texto.split(',')]
        if len(partes) != 3:
            await update.message.reply_text("⚠️ Formato incorrecto. Envía exactamente 3 valores separados por comas: Asistencias, PorcentajeTL, Pérdidas")
            return
        
        assists, ft_pct, turnovers = partes
        
        # Aplicación de la fórmula analítica
        score = (assists * 1.5) + (ft_pct * 0.1) - (turnovers * 2)
        
        await update.message.reply_text(
            f"📊 **Reporte de Análisis:**\n"
            f"• Asistencias: {assists}\n"
            f"• FT%: {ft_pct}%\n"
            f"• Pérdidas: {turnovers}\n\n"
            f"🔥 **Valor Estimado:** {score:.2f}"
        )
    except ValueError:
        await update.message.reply_text("⚠️ Por favor, utiliza solo números separados por comas. Ejemplo: 6, 75.5, 3")

if __name__ == '__main__':
    # Obtiene el token de forma segura desde las variables de la nube
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        print("Error: Falta configurar el TELEGRAM_TOKEN.")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calcular))
    
    print("Central Analítica activa...")
    application.run_polling()
      
