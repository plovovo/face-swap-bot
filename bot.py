import logging
import asyncio
import nest_asyncio  
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters
from face_swapper import FaceSwapper
from utils import image_from_bytes, image_to_bytes

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

TOKEN = "token" 
swapper = FaceSwapper()
user_photos = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь два фото — сначала лицо-источник, потом фото для подмены.")

# обработка фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_bytes = await file.download_as_bytearray()

    if user_id not in user_photos:
        user_photos[user_id] = {"source": file_bytes, "target": None}
        await update.message.reply_text("Окей, получил лицо-источник. Теперь пришли фото, на которое надо подменить лицо.")
    else:
        user_photos[user_id]["target"] = file_bytes
        await update.message.reply_text("Подменяю лицо...")

        try:
            source_img = image_from_bytes(user_photos[user_id]["source"])
            target_img = image_from_bytes(user_photos[user_id]["target"])
            swapped = swapper.swap_faces(source_img, target_img)
            swapped_bytes = image_to_bytes(swapped)

            await update.message.reply_photo(photo=swapped_bytes)
        except Exception as e:
            await update.message.reply_text(f"Ошибка при замене лица: {e}")
        finally:
            user_photos.pop(user_id)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    await app.run_polling(close_loop=False)

import asyncio
import nest_asyncio
nest_asyncio.apply()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

