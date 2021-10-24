# Инструкция по разворачиванию приложения: #
1. Клонировать репозиторий в удобном месте: git clone https://github.com/Tvo-Po/fabrique_st.git
2. Создать файл с переменными окружения /test_case/test_case/.env
3. В этом файле заполнить поля:
    * SECRET_KEY (https://djecrety.ir/)
    * DB_NAME (POSTGRES_DB из docker-compose)
    * DB_USER (POSTGRES_USER из docker-compose)
    * DB_USER_PASS (POSTGRES_USER из docker-compose)
    * DB_HOST (db dependency name, pgsql_db - по умолчанию)
    * DB_PORT (5432 по умолчанию)
4. Запустить контейнеры командой: docker-compose up (при первом разворачивании бэкэнд обычно подимается быстрее БД, если он не схватил порты - дождитесь разворачивания postgre и перезапустите контейнеры - CTRL+C, docker-compose up)
5. После того, как сервер запустился в другом терминале выполнить команду: docker exec -it django_backend bash
6. Запустить скрипт на заполнение базы данных: python db_script.py
----------------------
# Документация по API: #
* ### api/polls/ ###
   * Методы: GET
   * Описание: Выводит список опросов, которые еще не завершились.
   * Доступ: Все
* ### api/polls/`<slug:slug>`/ ###
   * Методы: GET
   * Описание: Выводит полную информацию по опросу. Опрос выбирается по своему полю slug.
   * Доступ: Все
* ### api/polls/`<slug:slug>`/pass/ ###
   * Методы: POST
   * Описание: Ссылка на прохождение анкеты. Пользователь выбирает анонимное или не анонимное прохождение опроса и отправляет ответы на вопросы. При анонмном прохождении нельзя увидеть данное заполнение в своей статистике.
   * Доступ: Все
   * Формат запроса: 
```json
{
    "amonymous": "False",
    "answers": [
        {
            "number": 1,
            "text": null,
            "chosen_answers": [
                {
                    "text": 8
                },
                {
                    "text": 20
                }
            ]
        },
        {
            "number": 2,
            "text": "Ничего общего",
            "chosen_answers": []
        },
        {
            "number": 3,
            "text": null,
            "chosen_answers": [
                {
                    "text": "Грибы"
                }
            ]
        }
    ]
}
```

* ### api/polls-admin/ ###
   * Методы: POST
   * Описание: Позволяет администратору создать опрос. При этом запрос можно передавать в формате nested json - то есть помещать все многозначные зависимости в массив.
   * Доступ: Администраторы
   * Формат запроса: 
```json
{
    "slug": "performance_coal_slide",
    "title": "Performance coal slide",
    "end_date": "2022-01-14",
    "questions": [
        {
            "number": 1,
            "text": "Arise engineer size false hi cabinet threaten japanese invest suppose live off application wish join?",
            "type": "MCH",
            "options": [
                {
                    "text": "Trace intensity."
                },
                {
                    "text": "Committee system unlike."
                },
                {
                    "text": "Unlikely off charity straight exhibit."
                }
            ]
        },
        {
            "number": 2,
            "text": "Lawsuit approval certain presence energy declare union trace dramatically gear headline identify?",
            "type": "TXT",
            "options": []
        },
        {
            "number": 3,
            "text": "Visit funding duty catch arrive essentially?",
            "type": "SCH",
            "options": [
                {
                    "text": "Participation major."
                },
                {
                    "text": "Relation gang."
                },
                {
                    "text": "Jew each or."
                },
                {
                    "text": "My collapse anywhere school peak here."
                },
                {
                    "text": "Prime index swear."
                }
            ]
        }
    ]
}
```

* ### api/polls-admin/`<slug:slug>`/ ###
   * Методы: PUT, PATCH, DELETE
   * Описание: Позволяет администратору редактировать опрос. Также, как и в предыдущем api можно работать с nested json, если зависимый объект уже существует, то у него просто поменяются поля (если что-то было изменено), а если не существует, то объект будет создан в процессе сериализации. Если какие-то зависимые сущности не указаны, то они остануться без изменений. При удалении все зависимые сущности также удаляются.
   * Доступ: Администраторы

* ### api/passed-polls/`<slug:slug>`/ ###
   * Методы: GET
   * Описание: Пользователь видит пройденные им опросы, за исключением тех, что он прошел анонимно.
   * Доступ: Авторизированные пользователи

* ### api/passed-polls/`<slug:slug>`/ ###
   * Методы: GET
   * Описание: Пользователь видит все прохождения с детальной информацией по данному опросу.
   * Доступ: Авторизированные пользователи

* ### api/token/ ###
   * Методы: POST
   * Описание: Отправляя валидные имя пользователя и паспорт, пользователь получает токен, который при помещении в заголовке (например с помощью Postman - вкладка Headers Authorization: Bearer `token` ), авторизирует вас на всех страницах на определенном промежутке времени.
   * Доступ: Авторизированные пользователи
