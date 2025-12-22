from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

with open("lab5/token.txt") as f:
    TOKEN = f.read()

import io
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "pixelsort"))
from corruption2 import corrupt_image

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "AWAITING TO RECEIVE AN IMAGE..."
    )

async def destroy_photo(update: Update, context: CallbackContext) -> None:
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()

        caption = update.message.caption
        if caption and 0 <= int(caption) <= 100:
            processed_bytes = corrupt_image(photo_bytes, tameness=int(caption))
        else:
            processed_bytes = corrupt_image(photo_bytes)

        await update.message.reply_photo(photo=processed_bytes, 
            caption="THANK YOU FOR YOUR CONTENT"
        )
    except Exception as e:
        print(e)
        await update.message.reply_text("SOMETHING WENT WRONG")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, destroy_photo))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        lambda update, context: update.message.reply_text("THIS IS NOT INCLUDED IN MY PROGRAMMING")
    ))

    print("Brace for impact")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()