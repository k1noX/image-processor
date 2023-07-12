# Сервер файловой системы

Основные использованные библиотеки:
1. Flask.
2. SQLAlchemy.
3. Psycopg2.

Структура проекта:
```
├── README.md
├── main.py
├── Db
│   ├── Mapper.py
│   └── SessionMaker.py
├── Files
│   └── Utils.py
├── Config
│   └── Config.py
├── App
│   └── Api.py
├── requirements.txt
└── config.ini
```

* Api - инициализация API Flask.
* Db - файлы работы с ORM и сессиями БД.
* Files - вспомогательные функции для работы с файлами.
* Config - классовые компоненты, выполняющие загрузку файла конфигурации.
* main.py - выполняемая часть приложения.

## Запуск 

1. Клонирование репозитория.
2. `pip install requirements.txt`.
3. Создание базы данных: `python Db/init.py`.
4. Запуск сервера `python main.py`.

## Запуск в контейнере

1. Клонирование репозитория.
2. `docker-compose build`.
3. `docker-compose up -d`.
3. `docker-compose exec app python Db/init.py`.

## Использование
### Эндпоинты
#### POST /

REQUEST (FORM)
```json
{
  "file": "файл",
  "name": "имя файла",
  "comment": "комментарий"
}
```

RESPONSE
```json
{
  "comment": "забытый документ",
  "created_at": "Tue, 04 Jul 2023 07:43:06 GMT",
  "extension": ".pdf",
  "name": "subka",
  "path": "docs\\",
  "size": 244641,
  "updated_at": "Tue, 04 Jul 2023 07:56:43 GMT"
}
```
#### GET /

RESPONSE
```json
[
  {
    "comment": "кто-то просит вернуть полтос",
    "created_at": "Tue, 04 Jul 2023 07:43:20 GMT",
    "exists": true,
    "extension": ".png",
    "id": 36,
    "name": "poltos",
    "path": "screenshots\\discord\\",
    "size": 14494,
    "updated_at": "Tue, 04 Jul 2023 07:44:50 GMT"
  },
  {
    "comment": "исходный код апи",
    "created_at": "Tue, 04 Jul 2023 07:43:13 GMT",
    "exists": true,
    "extension": ".py",
    "id": 35,
    "name": "Api",
    "path": "code\\",
    "size": 14869,
    "updated_at": "Tue, 04 Jul 2023 07:46:21 GMT"
  }]
```

#### GET /path/[path]

Нахождение файла по его пути внутри файловой системы

RESPONSE
```json
{
  "comment": "кто-то просит вернуть полтос",
  "created_at": "Tue, 04 Jul 2023 07:43:20 GMT",
  "exists": true,
  "extension": ".ext",
  "id": 36,
  "name": "filename",
  "path": "path",
  "size": 14494,
  "updated_at": "Tue, 04 Jul 2023 07:44:50 GMT"
}
```


#### POST /path/[path]

Добавление файла по пути в файловой системе

REQUEST (FORM)
```json
{
  "file": "файл",
  "name": "имя файла",
  "comment": "комментарий"
}
```

#### GET /path/[path]/download

Загрузка файла по его пути

RESPONSE - File


#### GET /file/[id]/download

Загрузка файла по его id

RESPONSE - File


#### GET /file/[id]

Нахождение файла по его id в БД

RESPONSE
```json
{
  "comment": "кто-то просит вернуть полтос",
  "created_at": "Tue, 04 Jul 2023 07:43:20 GMT",
  "exists": true,
  "extension": ".ext",
  "id": 36,
  "name": "filename",
  "path": "path",
  "size": 14494,
  "updated_at": "Tue, 04 Jul 2023 07:44:50 GMT"
}
```

#### PUT /file/[id]

Обновление данных о файле по его id

REQUEST (FORM)
```json
{
  "name": "имя файла",
  "comment": "комментарий",
  "path": "путь к файлу"
}
```

RESPONSE
```json
{
  "comment": "кто-то просит вернуть полтос",
  "created_at": "Tue, 04 Jul 2023 07:43:20 GMT",
  "exists": true,
  "extension": ".ext",
  "id": 36,
  "name": "filename",
  "path": "path",
  "size": 14494,
  "updated_at": "Tue, 04 Jul 2023 07:44:50 GMT"
}
```


#### GET /path/[path]/

Поиск файлов внутри указанного пути path.

RESPONSE
```json
[
  {
    "comment": "кто-то просит вернуть полтос",
    "created_at": "Tue, 04 Jul 2023 07:43:20 GMT",
    "exists": true,
    "extension": ".png",
    "id": 36,
    "name": "poltos",
    "path": "path",
    "size": 14494,
    "updated_at": "Tue, 04 Jul 2023 07:44:50 GMT"
  },
  {
    "comment": "исходный код апи",
    "created_at": "Tue, 04 Jul 2023 07:43:13 GMT",
    "exists": true,
    "extension": ".py",
    "id": 35,
    "name": "Api",
    "path": "path",
    "size": 14869,
    "updated_at": "Tue, 04 Jul 2023 07:46:21 GMT"
  }]
```

#### PUT /path/[path]

Обновление данных о файле

REQUEST (FORM)

```json
{
  "name": "имя файла",
  "comment": "комментарий",
  "path": "путь к файлу"
}
```

RESPONSE
```json
{
  "comment": "кто-то просит вернуть полтос",
  "created_at": "Tue, 04 Jul 2023 07:43:20 GMT",
  "exists": true,
  "extension": ".ext",
  "id": 36,
  "name": "filename",
  "path": "path",
  "size": 14494,
  "updated_at": "Tue, 04 Jul 2023 07:44:50 GMT"
}
```


#### POST /refresh

Актуализация хранилища

RESPONSE
```json
{
  "message": "Storage Has Been Refreshed! 10 rows affected!"
}
```