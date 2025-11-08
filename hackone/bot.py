from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN = '8211484348:AAGTQx1ZpqaOg11EwbRSR6v_qt5fT-DdLpY'  # tu token real
BACKEND_URL = 'http://localhost:5000/api/registrar_chat'  # ajustá si usás otra IP

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hola, por favor enviá tu número de teléfono para recibir alertas.")

# Captura el número y lo envía al backend
async def recibir_telefono(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telefono = update.message.text
    chat_id = update.message.chat_id

    try:
        response = requests.post(BACKEND_URL, json={
            "telefono": telefono,
            "chat_id": str(chat_id)
        })
        if response.status_code == 200:
            await update.message.reply_text("✅ Número registrado correctamente.")
        else:
            await update.message.reply_text("⚠️ Hubo un error al registrar tu número.")
    except Exception as e:
        await update.message.reply_text("❌ No se pudo conectar con el servidor.")

# Configuración del bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_telefono))

    print("🤖 Bot iniciado...")
    app.run_polling()