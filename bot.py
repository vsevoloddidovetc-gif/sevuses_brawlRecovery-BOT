import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TAG, NAME, TROPHIES, CLUB, DEVICE, REASON = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Welcome to Brawl Recovery Assistant!\n\n"
        "I'll help format your request for Supercell Support.\n\n"
        "First, what is your Player Tag? (e.g., #ABC1234)"
    )
    return TAG

async def get_tag(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['tag'] = update.message.text
    await update.message.reply_text("Got it! What was your exact In-Game Nickname?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text("How many Trophies did the account roughly have?")
    return TROPHIES

async def get_trophies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['trophies'] = update.message.text
    await update.message.reply_text("What was your Club Name? (Send 'None' if you weren't in one):")
    return CLUB

async def get_club(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['club'] = update.message.text
    await update.message.reply_text("What exact Device Model did you play on? (e.g., Samsung M14):")
    return DEVICE

async def get_device(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['device'] = update.message.text
    await update.message.reply_text("Briefly explain how access was lost (e.g., changed phones, device reset):")
    return REASON

async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reason = update.message.text
    d = context.user_data

    summary = (
        "<b>Copy and paste this message into Supercell Support:</b>\n\n"
        "----------------------------------------\n"
        f"<b>Player Tag:</b> {d['tag']}\n"
        f"<b>Nickname:</b> {d['name']}\n"
        f"<b>Trophies:</b> {d['trophies']}\n"
        f"<b>Club:</b> {d['club']}\n"
        f"<b>Device:</b> {d['device']}\n"
        f"<b>Reason:</b> {reason}\n"
        "----------------------------------------\n\n"
        "<i>Tip: Keep your Google Play or App Store purchase receipts ready if you ever bought Gems or Passes!</i>"
    )

    await update.message.reply_html(summary)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Cancelled. Send /start to begin again.")
    return ConversationHandler.END

if __name__ == '__main__':
    # Paste your raw token string from @BotFather right inside the quotes below:
    BOT_TOKEN = "8849102786:AAFUmBjrkKByrGSGerX8_GAjfzBgYAtkqXY"

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TAG: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tag)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            TROPHIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_trophies)],
            CLUB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_club)],
            DEVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_device)],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    print("Bot is starting...")
    app.run_polling()