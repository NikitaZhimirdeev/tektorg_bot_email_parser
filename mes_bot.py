from aiogram import Bot, executor, types
from aiogram.dispatcher import Dispatcher
from datetime import datetime
import asyncio
import settings

# Инициализировать бота и диспетчера

bot = Bot(token=settings.Token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def START(message: types.Message):
    await message.answer('Бот будет направлять вам ежедневную сводку по опубликованным конкурентным закупкам '
                         'на площадке ТЭК-Торг по состоянию на 19:00 МСК. Для активации введите: /start')

# Функция отправки файла
async def echo():
    # Объявляем путь/имя файла
    filename = f'RN_file/Сводка по закупкам РН за {datetime.now().strftime("%d.%m.%Y")}.csv'
    # Открываем файл в байтовом виде
    file_to_send = open(filename, 'rb')
    # Отправляем сообщение с файлом
    await bot.send_document(chat_id=settings.chat_id, document=file_to_send)

# Функция записи бота
def get_bot():
    # Объявяляем и запускаем цикл событий
    loop = asyncio.get_event_loop()
    loop.create_task(echo())
    # Запускаем бота для отправки сообщения
    executor.start_polling(dp, skip_updates=True)

