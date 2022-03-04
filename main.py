from datetime import datetime, timedelta
import time
from multiprocessing import Process
import find_data
import mes_email
import mes_bot
import os
import create_file
import additional_scripts

# Исполнительная функция, запускающая все вспомогательные
def main():
    # Поиск текущего расположения
    dir_path = os.path.dirname(os.path.abspath(__file__)) #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # Получаем данные все закупок
    DATA = find_data.get_data()

    # Проверяем существование таблицы
    additional_scripts.chek_table(dir_path)

    # Проверка на дубли в БД и добавление новых записей
    additional_scripts.chek_and_append_info_table(dir_path, DATA)

    # Загружаем БД на диск
    additional_scripts.load_BD(dir_path)

    #filename = os.path.join(dir_path, f'Сводка по закупкам РН за {datetime.now().strftime("%d.%m.%Y")}.csv') #$
    # Формируем имя файла по текущей дате
    filename = f'RN_file/Сводка по закупкам РН за {datetime.now().strftime("%d.%m.%Y")}.csv'
    print(filename)

    # Запись шапки в файл
    create_file.head(filename)

    # Запись данных о всех закупках
    create_file.save_file(DATA, filename)

    # Отправляем файл на почту
    mes_email.get_email(filename)

    # Объявляем экзепляр процесса для удобного запуска и отключения ТГ бота
    p = Process(target=mes_bot.get_bot)

    # Запуск процесса (Отправление сообщение в боте ТГ)
    p.start()

    # ожидаем, чтобы ботуспел отправить файл
    time.sleep(60)

    # Закрываем процесс работы с ТГ ботом
    p.kill()

if __name__ == '__main__':
    main()



