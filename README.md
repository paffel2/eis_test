# eis_test

Задание для компании ЕИС ЖКХ.

## Запуск
    docker compose up

## Эндпоинты

### Дом
    GET /houses/ - получение списка домов
    POST /houses/ - добавление дома
    UPDATE /house/{id} - обновление дома
    DELETE /house/{id} - удаление дома
    GET /houses/{id} - получение информации о доме
    GET /houses/{id}/calculate_bills/ - запустить рассчет квартплаты
    GET /houses/{id}/get_bill_process/ - проверить статус рассчета
    GET /houses/{id}/get_bills/ - получить счета


### Квартиры
    GET /houses/{house_pk}/apartments/ - получить список квартир дома
    POST /houses/{house_pk}/apartments/ - добавить квартиру
    PUT /houses/{house_pk}/apartments/{id} - обновить список квартиру дома
    DELETE /houses/{house_pk}/apartments/{id} - удалить квартиру
    GET /houses/{house_pk}/apartments/{id} - получение информации о квартире
    GET /houses/{house_pk}/apartments/{id}/get_bill/ - получение счета


### Счетчики
    GET /houses/{house_pk}/apartments/{apartment_pk}/counters/ - получить список счетчиков
    POST /houses/{house_pk}/apartments/{apartment_pk}/counters/ - добавить счетчик
    GET /houses/{house_pk}/apartments/{apartment_pk}/counters/{id} - получение информации о счетчике
    PUT /houses/{house_pk}/apartments/{apartment_pk}/counters/{id} - обновить счетчик
    DELETE /houses/{house_pk}/apartments/{apartment_pk}/counters/{id} - удалить счетчик

### Показания
    GET /houses/{house_pk}/apartments/{apartment_pk}/counters/{counter_pk}/readings/ - список показаний счетчика
    POST /houses/{house_pk}/apartments/{apartment_pk}/counters/{counter_pk}/readings/ - добавить показания счетчика
    GET /houses/{house_pk}/apartments/{apartment_pk}/counters/{counter_pk}/readings/{id}/ - получение информации о показаниях
    PUT /houses/{house_pk}/apartments/{apartment_pk}/counters/{counter_pk}/readings/{id}/  - обновить показания счетчика
    DELETE /houses/{house_pk}/apartments/{apartment_pk}/counters/{counter_pk}/readings/{id}/ - удалить показания счетчика

### Тарифы
    GET /rates/ - список тарифов
    POST /rates/ - добавить тариф
    GET /rates/{id}/ - получить информацию о тарифе
    PUT /rates/{id}/ - обновить информацию о тарифе
    DELETE /rates/{id}/ - удалить тариф

### Openapi

Для открытия страницы с апи воспользуйтесь [ссылкой](http://127.0.0.1:8000/).

##  Состав проекта

    /eis/ - папка с Django приложение, содержит реализацию эндпоинтов, моделей, сериализаторов, классов View, задачи отправляемой Celery
    /eis_test/ - основная папка, содержит настройки сервера, настройки celery
    Dockerfile - файл Docker для создания образа с сервером
    docker-compose.yml - файл docker-compose для запаска контейнеров
    requirements.txt - файл, содержащий список необходимых библиотек 

## Используемый стек
    Django
    Django rest framework
    Celery
    Redis
    PosgreSQL
    Docker

