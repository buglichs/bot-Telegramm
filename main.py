from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, ChatMemberHandler
import logging

# --- CONFIGURACIÓN ---
TOKEN = "7351788464:AAGD4o2k6iB2Xf-kTZ_qNrQYdVEb_qq1vSw"
VIP_LINK = "https://t.me/+htun0-AWbb44OGMx"

# Contador de compartidos por usuario
user_progress = {}

# Activamos logging
logging.basicConfig(level=logging.INFO)


# --- Cuando un usuario entra al grupo ---
async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member
    if chat_member.new_chat_member.status == "member":
        user = chat_member.from_user
        user_progress[user.id] = 0

        # Enviarle mensaje privado
        try:
            keyboard = [[
                InlineKeyboardButton("✅ Ya compartí", callback_data="shared")
            ]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=user.id,
                text=
                (f"👋 Hola {user.first_name}!\n\n"
                 "Para acceder al grupo VIP, debes compartir este grupo al menos 3 veces.\n"
                 "Cada vez que lo hagas, presiona el botón '✅ Ya compartí'."),
                reply_markup=reply_markup)
        except:
            print(
                "No se pudo enviar mensaje privado (debe iniciar el bot con /start)"
            )


# --- Botón "Ya compartí" ---
async def button_pressed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    user_progress[user_id] = user_progress.get(user_id, 0) + 1

    if user_progress[user_id] >= 3:
        await query.message.reply_text(
            f"🎉 ¡Gracias por compartir 3 veces!\nAquí tienes acceso al grupo VIP:\n{VIP_LINK}\n\nNo compartas este enlace con nadie."
        )
    else:
        await query.message.reply_text(
            f"🔁 Has registrado {user_progress[user_id]}/3 compartidos.\nSigue compartiendo y presiona el botón cada vez."
        )


# --- Comando /start obligatorio para poder escribirle al usuario ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_progress[user_id] = 0

    keyboard = [[
        InlineKeyboardButton("✅ Ya compartí", callback_data="shared")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 ¡Bienvenido!\nDebes compartir el grupo al menos 3 veces para acceder al grupo VIP.\n\nPresiona el botón cada vez que compartas.",
        reply_markup=reply_markup)


# --- INICIO DEL BOT ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_pressed))
app.add_handler(
    ChatMemberHandler(greet_new_member, ChatMemberHandler.CHAT_MEMBER))

app.run_polling()
