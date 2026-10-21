import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from google import genai

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

ai_client = genai.Client()

# /start command with interactive buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔄 Recover Account", callback_data="recover")],
        [InlineKeyboardButton("❓ Common Issues", callback_data="faq")],
        [InlineKeyboardButton("📞 Contact Support", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👋 Welcome to **Brawl Stars Recovery Bot**!\n\n"
        "I can help you navigate account recovery steps or answer your questions. "
        "Choose an option below:"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "recover":
        await query.edit_message_text(text="🔄 Let's start your recovery! Please send me your old account Tag (e.g., #ABC123XYZ).")
    elif query.data == "faq":
        await query.edit_message_text(text="❓ **Common Issues:**\n- Lost Supercell ID? Make sure you check your email spam folder.\n- Banned account? Support requests must go through the in-game help menu.")
    elif query.data == "support":
        await query.edit_message_text(text="📞 For direct assistance, please describe your issue here, and our AI assistant will help you out!")

# AI chat handler for normal text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    response = ai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"You are a helpful and smart assistant for Brawl Stars account recovery and support. Answer this user clearly and concisely: {user_message}",
    )
    
    await update.message.reply_text(response.text)

if __name__ == "__main__":
    token = os.environ.get("BOT_TOKEN")
    
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    application.run_polling()
