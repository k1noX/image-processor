# Обработка изображений и файловый сервер

Основные использованные технологии:
1. Flask.
2. uWSGI.
3. PostgreSQL.
4. RabbitMQ.
5. Nginx.

## Запуск 

1. Клонирование репозитория.
2. `docker-compose up --build`.

## Структура проекта 

├── README.md
├── docker-compose.yml
├── config
│   ├── file-storage
│   │   ├── conf.yml
│   │   └── wsgi.ini
│   ├── image-processor
│   │   ├── conf.yml
│   │   └── wsgi.ini
│   ├── worker
│   ├── nginx.conf
│   ├── postgresql.env
│   └── rabbitmq.env
├── file-storage
│   ├── src
│   │   ├── config
│   │   ├── injectors
│   │   ├── services
│   │   ├── models
│   │   ├── routers
│   │   ├── utils
│   │   └── app.py
│   ├── file-storage.Dockerfile
│   └── requirements.txt
└── image-processor
    ├── src
    │   ├── algorithms
    │   ├── config
    │   ├── handler
    │   ├── injectors
    │   ├── services
    │   ├── models
    │   ├── routers
    │   ├── scripts
    │   └── app.py
    ├── image-processor.Dockerfile
    ├── worker.Dockerfile
    └── requirements.txt

## Использование

## API
### FileServer
#### POST /api/file-server/

> Добавление файла на сервер.

REQUEST
```json
{
  "name": "имя файла",
  "comment": "комментарий"
}
```
> Файл прикрепляется к форме в поле "file".


RESPONSE
```json
{
  "id": 1,
  "comment": "doc",
  "extension": ".pdf",
  "name": "subka",
  "size": 244641,
  "created_at": "Tue, 04 Jul 2023 07:43:06 GMT",
  "updated_at": "Tue, 04 Jul 2023 07:56:43 GMT"
}
```
#### GET /api/file-server/

> Получение списка всех файлов с сервера.

RESPONSE
```json
[
  {
    "id": 36,
    "name": "filename",
    "extension": ".ext",
    "comment": "описание",
    "size": 14494,
    "created_at": "Tue, 04 Jul 2023 07:43:20 GMT",
    "updated_at": "Tue, 04 Jul 2023 07:44:50 GMT"
  },
  {
    "id": 1,
    "comment": "doc",
    "extension": ".pdf",
    "name": "subka",
    "size": 244641,
    "created_at": "Tue, 04 Jul 2023 07:43:06 GMT",
    "updated_at": "Tue, 04 Jul 2023 07:56:43 GMT"
  }]
```

#### GET /api/file-server/[id]

> Нахождение файла по его id.

RESPONSE
```json
{
  "id": 36,
  "name": "filename",
  "extension": ".ext",
  "comment": "описание",
  "size": 14494,
  "created_at": "Tue, 04 Jul 2023 07:43:20 GMT",
  "updated_at": "Tue, 04 Jul 2023 07:44:50 GMT"
}
```

#### GET /api/file-server/[id]/download

> Загрузка файла по его id.

RESPONSE - File

#### PATCH /api/file-server/[id]

> Обновление данных о файле по его id.

REQUEST
```json
{
  "name": "имя файла",
  "comment": "комментарий"
}
```

RESPONSE
```json
{
  "id": 36,
  "name": "filename",
  "extension": ".ext",
  "comment": "описание",
  "size": 14494,
  "created_at": "Tue, 04 Jul 2023 07:43:20 GMT",
  "updated_at": "Tue, 04 Jul 2023 07:44:50 GMT"
}
```



## API
### ImageProcessing
#### GET /api/image-processing/

> Получение списка всех задач.

REQUEST
```json
[
  {
    "id": 1,
    "source_id": 1,
    "result_id": null,
    "status": "pending",
    "algorithm": "resize",
    "params": {
        "width": 128,
        "height": 128
    }
  },
  {
    "id": 2,
    "source_id": 3,
    "result_id": 4,
    "status": "finished",
    "algorithm": "resize",
    "params": {
        "width": 128,
        "height": 128
    }
  },
  {
    "id": 3,
    "source_id": 3,
    "result_id": null,
    "status": "error",
    "algorithm": "flip",
    "params": null
  },
  {
    "id": 4,
    "source_id": 3,
    "result_id": null,
    "status": "processing",
    "algorithm": "flip",
    "params": null
  }
]
```

#### POST /api/image-processing/

> Создание задачи.

REQUEST
```json
{
  "file_ids": [1, 2, 3],
  "algorithm": "resize",
  "params": {
    "width": 128,
    "height": 128
  }
}
```

RESPONSE
```json
{
  "task_ids": [1, 2, 3]
}
```

#### GET /api/image-processing/[id]

> Получение задачи по id.

RESPONSE
```json
{
  "id": 1,
  "source_id": 1,
  "result_id": null,
  "status": "pending",
  "algorithm": "resize",
  "params": {
    "width": 128,
    "height": 128
  }
}
```

#### POST /api/image-processing/[id]/restart

> Перезапуск выполнения задачи, завершённой с ошибкой.

RESPONSE
```json
{
  "id": 1,
  "source_id": 1,
  "result_id": null,
  "status": "pending",
  "algorithm": "resize",
  "params": {
    "width": 128,
    "height": 128
  }
}
```
