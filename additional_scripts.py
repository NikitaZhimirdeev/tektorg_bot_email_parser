import settings
import re
from sqliter import SQLighter
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import os
import io


# Проверка на существование таблицы, если ее нет, то создаем
def chek_table(dir_path):
    db = SQLighter(os.path.join(dir_path, 'databaseParser.db'))
    # Проверка существования таблицы
    all_table = db.all_table()
    ALL_TABLE = []
    for table in all_table:
        ALL_TABLE.append(re.sub("[^A-Za-z_]", "", str(table)))
    # Создание таблицы если ее нет
    if not ('RN_DATA' in ALL_TABLE):
        db.create_table()

# Проверка на дубли в БД и добавление новых записей
def chek_and_append_info_table(dir_path, DATA):
    db = SQLighter(os.path.join(dir_path, 'databaseParser.db'))

    for row in DATA:
        if not db.allpost_exists(row['number_zak']):
            db.add_message(row)
            print(row)

# Скачиваем БД
def download_BD():
    # возможности, которыми будет обладать сервис
    SCOPES = ['https://www.googleapis.com/auth/drive']
    # путь к файлу с ключами сервисного аккаунта
    SERVICE_ACCOUNT_FILE = 'rndrivedb-0b877feafaef.json'

    # учетные данные
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    with open('db_id.txt', 'r') as file:
        file_id = file.read()

    # file_id = '1MXP6tqkK87kp3r8NKuLwYZm2W1J1SfYM'
    request = service.files().get_media(fileId=file_id)
    filename = 'databaseParser.db'
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    service.files().delete(fileId=file_id).execute()

# Загружаем БД на диск
def load_BD(dir_path):
    # возможности, которыми будет обладать сервис
    SCOPES = ['https://www.googleapis.com/auth/drive']
    # путь к файлу с ключами сервисного аккаунта
    SERVICE_ACCOUNT_FILE = 'rndrivedb-0b877feafaef.json'

    # учетные данные
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    # удаление лишней бд
    try:
        with open('db_id.txt', 'r') as file:
            file_id = file.read()
        service.files().delete(fileId=file_id).execute()
    except:
        pass

    # указываем путьв БД
    folder_id = settings.folder_ID
    name = 'databaseParser.db'
    file_path = 'databaseParser.db'
    file_metadata = {
        'name': name,
        'parents': [folder_id]
    }
    # Создаем запрос к диску
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # перезаписываем id БД
    with open('db_id.txt', 'w') as file:
        file.write(r['id'])

    # os.remove(os.path.join(dir_path, 'databaseParser.db'))
