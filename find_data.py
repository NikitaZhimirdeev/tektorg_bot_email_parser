import time
import requests
from bs4 import BeautifulSoup as BS4
import lxml
from data_replace import data_repl
from datetime import datetime, timedelta

# Задаем User-Agent
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

# Функция сбора данных
def get_data():
    # Определяем сегодняшнюю и вчерашнюю даты
    now = datetime.now()
    dat_today = now.strftime("%d.%m.%Y")
    dat_yesterday = (datetime.now() - timedelta(1)).strftime("%d.%m.%Y")

    # Создаем ссылку запроса
    URL = f"https://www.tektorg.ru/rosneft/procedures?dpfrom={dat_yesterday}&dpto={dat_today}&sort=datestart&order=desc&limit=500"
    print(URL)
    # Отправляем запрос для получения кода страницы
    resp = requests.get(URL, headers=HEADERS)
    soup = BS4(resp.text, 'lxml')
    # Объявляем список для сбора данных
    DATA = []
    # Ищем все элементы с закупок
    conts = soup.find_all('div', class_='section-procurement__item')#.find_all('tr', class_='section-procurement__row')
    j = 1
    # Цикл сбора данных из каждого элемента закупки
    for cont in conts[0:30]:
        print(j)
        j += 1
        # Получаем ссылку на закупку
        href = f"https://www.tektorg.ru{cont.find('a', class_='section-procurement__item-title').get('href')}"
        print(href)
        print()
        # Получаем номер закупки
        number_zak = cont.find('div', class_='section-procurement__item-numbers').text.strip().split(':')[1].strip()
        # Получаем Название закупки
        Title = cont.find('a', class_='section-procurement__item-title').text.strip()
        # Получаемимя органзатора
        organizer = cont.find('div', class_='section-procurement__item-description').find('a').text.strip().upper()
        # Получаем даты публикации, окончания приема и подведения итогов
        DATAS = cont.find_all('div', class_='section-procurement__item-dateTo')
        date_publication = DATAS[0].text.strip().split('          ')[1].strip()#.split(' ')[0]
        end_date = DATAS[1].text.strip().split('          ')[1].strip()#.split(' ')[0]
        summing_results = DATAS[2].text.strip().split('          ')[1].strip()#.split(' ')[0]
        # Получаем столбик дополнительно
        try:
            additionally = cont.find('div', class_='section-procurement__item-totalPrice').text.strip().replace('₽', '').strip()
        except:
            additionally = ''
        # Получаем код страницы одной закупки
        try:
            resp_c = requests.get(href, headers=HEADERS)
        except:
            try:
                print('sleep 1')
                time.sleep(10)
                resp_c = requests.get(href, headers=HEADERS)
            except:
                try:
                    print('sleep 2')
                    time.sleep(20)
                    resp_c = requests.get(href, headers=HEADERS)
                except:
                    try:
                        print('sleep 4')
                        time.sleep(40)
                        resp_c = requests.get(href, headers=HEADERS)
                    except:
                        print('sleep 8')
                        time.sleep(80)
                        resp_c = requests.get(href, headers=HEADERS)

        soup_c = BS4(resp_c.text, 'lxml')
        # Получаем заказчика
        customer_trs = soup_c.find('div', class_='procedure__lot-item').find('table',
                                                                             class_='procedure__item-table').find_all(
            'tr')
        customer = ''
        for customer_tr in customer_trs:
            td = customer_tr.find('td').text.strip()
            if td == 'Заказчик:':
                customer = customer_tr.find('div').text.strip().upper()

        # Получение данных контактного лица
        contact_person_trs = soup_c.find('div', id='orgInfo').find('table',
                                                                   class_='procedure__item-table').find_all('tr')
        contact_person = ''
        for contact_person_tr in contact_person_trs:
            tds = contact_person_tr.find_all('td')
            if tds[0].text.strip() == 'ФИО контактного лица:':
                contact_person = tds[1].text.strip()

        customer_try = 'NaN'
        if (customer == '') and (organizer == ''):
            customer_try = customer

        # Приводим к необходимому виду
        organizer, customer, additionally = get_replace(organizer, customer, additionally)

        # Запись всех полученных данных в список в виде словаря
        DATA.append({
            'number_zak': number_zak,
            'Title': Title,
            'organizer': organizer,
            'date_publication': date_publication,
            'end_date': end_date,
            'summing_results': summing_results,
            'additionally': additionally,
            'customer': customer,
            'customer_try': customer_try,
            'contact_person': contact_person,
            'href': href
        })
    # Возвращение данных
    return DATA

# Функция удаления лишних слов
def get_replace(organizer, customer, additionally):
    for repl in data_repl:
        organizer = organizer.replace(repl, '').replace('82СРЗ', '82 СРЗ').strip()
        customer = customer.replace(repl, '').replace('82СРЗ', '82 СРЗ').strip()
    if additionally != '':
        additionally = f"{int(additionally.split(',')[0].replace(' ', '')) / 1000000} млн. руб."
    else:
        additionally = 'не публикуется'
    return organizer, customer, additionally
