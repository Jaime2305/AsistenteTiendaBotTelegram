
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from Bot_Menu import inicioConversacion, handle_message
from configuracion import TokenTelegram

app = ApplicationBuilder().token(TokenTelegram).build()

app.add_handler(CommandHandler(["iniciar","start","comenzar"], inicioConversacion))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot corriendo...")


app.run_polling()
