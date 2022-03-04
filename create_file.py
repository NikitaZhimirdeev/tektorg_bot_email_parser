import csv
import os

# Функция записи в файл шапки
def head(filename):
    # Объявляем все элементы шапки файла
    H = ['Номер закупки', 'Название', 'Организатор', 'Дата публикации процедуры',
         'Дата окончания приема заявок', 'Подведение итогов не позднее', 'Информация о НМЦ',
         'Заказчик', 'Заказчик_тру', 'ФИО контактного лица', 'ссылка на закупку']
    # Открываем файл на запись
    with open(filename, 'w', newline='') as f: #, encoding='utf8'
        # Объявление инструмента записи
        writer = csv.writer(f, delimiter=';')
        # Запись в файл
        writer.writerow(H)

# Запись всех элементов закупок
def save_file(prod, filename):
    # Открываем файл на запись
    with open(filename, 'a', newline='') as file:  # , encoding='utf8'
        # Объявление инструмента записи
        writer = csv.writer(file, delimiter=';')
        # Проходим по всем элементам списка, полученного при вызове данной функции
        for p in prod:
            # Запись одного лемента списка, в котором содержится словарь
            try:
                writer.writerow([
                    p['number_zak'], p['Title'], p['organizer'], p['date_publication'], p['end_date'],
                    p['summing_results'], p['additionally'], p['customer'], p['customer_try'], p['contact_person'], p['href']
                ])
            except:
                print(p)

