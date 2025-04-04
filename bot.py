
import logging
import csv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Взимаме токена от config.py
from config import BOT_TOKEN

# Зареждаме данните за стикер паковете
def load_packs():
    packs = []
    with open("packs.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            packs.append(row)
    return packs

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    packs = load_packs()
    buttons = [
        [InlineKeyboardButton(pack['name'], callback_data=f"pack_{i}")]
        for i, pack in enumerate(packs)
    ]
    await update.message.reply_text(
        "🎉 Welcome! Choose a sticker pack to view the free stickers:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("pack_"):
        index = int(data.split("_")[1])
        packs = load_packs()
        pack = packs[index]

        await query.message.reply_text(
            f"📦 *{pack['name']}*

Here are the free stickers:
{pack['free_links']}

"
            f"🔓 To unlock the full pack:
💸 Price: {pack['price_bgn']} BGN
"
            f"📥 Full pack: {pack['paid_link']}",
            parse_mode="Markdown"
        )

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
