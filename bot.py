
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler
import logging
from render import render_text_on_image, image_to_string
from io import BytesIO

import os


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! I respond with a picture to any message.')

async def respond_with_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = render_text_on_image("red_ebalo.png", update.message.text)
    await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=file)

async def image2string(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  
    

    file = await photo.get_file()  
    bio = BytesIO()          
    await file.download_to_memory(out=bio)   

    bio.seek(0)

    s = image_to_string(bio)

    await update.message.reply_text(s)

async def inline_respond_with_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.inline_query.query
    if not query:
        return
    
    xcom = "https://x.com"

    if xcom in query:

        results = [
            {
                "type": "article",
                "id": "1",
                "title": "fix xitter links",
                "description": query.replace(xcom, "https://fxtwitter.com"),
                "input_message_content": {
                    "message_text": query.replace(xcom, "https://fxtwitter.com")
                }
            }
        ]

        await context.bot.answer_inline_query(update.inline_query.id, results)

        return

    bot_info = await context.bot.get_me()

    file = render_text_on_image("red_ebalo.png", query)

    file_id = (await context.bot.send_sticker(chat_id=-1002471390283, sticker=file)).sticker.file_id
    results = [
        {
            "type": "sticker",
            "id": "1",
            "sticker_file_id": file_id 
        } 
    ]
    await context.bot.answer_inline_query(update.inline_query.id, results)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    picture_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, respond_with_picture)

    application.add_handler(start_handler)

    application.add_handler(MessageHandler(filters.PHOTO, image2string))
    application.add_handler(picture_handler)
    application.add_handler(InlineQueryHandler(inline_respond_with_sticker))

    application.run_polling()

if __name__ == '__main__':
    main()
