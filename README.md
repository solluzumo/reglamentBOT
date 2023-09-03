# Чат-бот

### Описание проекта

Цель проекта "Чат-бот справочник" заключается в упрощении работы с большим объемом документов. Бот позволяет пользователю искать нужные заголовки в регламентах и выдает содержимое этих заголовков.

### Устройство проекта

Проект имеет следующую структуру:
1. `server.py`: Файл с хэндлерами для обработки запросов пользователя (текстовые запросы и обработка клавиатуры).
2. `keyboards.py`: Файл, формирующий клавиатуру для удобного взаимодействия с пользователем.
3. `application scripts/set-id-to-title.py`: Файл, помогающий парсить заголовки и присваивать им определенные значения (id) для дальнейшего использования.
4. `application scripts/uatest.py`: Файл, преобразующий текст регламентов в словарь.
5. `classes.py`: Файл, описывающий классы, используемые в проекте, он так же содержит функции, преобразующие строку с данными в объект класса.
6. `search.py`: Файл, содержащий функции поиска данных по различным параметрам в файле accordance, а так же в текущем словаре.
7. `title_handler.py`: Файл, содержащий логику разделения на комплексные(заголовки,имеющие вложенность) и обычные заголовки, так же там описаны функции отправки сообщений, формирования текста, создания клавиатуры.

### Запуск проекта

Для запуска проекта необходимо установить все зависимости из файла `requirements.txt` и запустить бота командой `python main.py`.

### Зависимости

Проект использует следующие зависимости:
- `aiogram`: библиотека для создания ботов Telegram.
- `fuzzywuzzy`: библиотека для выполнения нечеткого сравнения строк.

### Функционал проекта

1. Поиск заголовков по запросу: Бот использует автоматическую обработку нечетких или неточных сравнений строк с помощью библиотеки `fuzzywuzzy` для поиска заголовков в регламентах, соответствующих запросу пользователя.

2. Клавиатура: Бот предоставляет клавиатуру, которая позволяет более подробно рассмотреть некоторые заголовки. Пользователь может выбрать заголовок и узнать в каком конкретном регламенте, пункте, подпункте и т.д. находится интересующая его информация.

3. Прикладные скрипты: В проекте предусмотрены два скрипта:`application scripts/set-id-to-title.py` и `application scripts/uatest.py`. Первый выписывает из регламента, представленного в виде словаря, заголовки в `accordance.txt`; Второй скрипт преобразует текст регламентов в словарь.

### Ошибки и исключения

Типичными ошибками являются ошибки при обращении к файлу регламента. Так как файл регламента представляется в виде словаря, при некорректном обращении к ключу или значению в словаре могут возникать соответствующие ошибки.

### Устройство файлов

Проект содержит несколько файлов с данными:
1. Файлы с регламентом: Файлы представляют собой словари, где ключ - название заголовка, значение - подзаголовки. Словарь может достигать 3-4 уровней вложенности и используется для легкого поиска. Название файлов соответствуют названию регламентов.
2. `accordance.txt`: Файл содержит соответствия id-заголовок-регламент.
3. Директории в `static/tables` имеют название id заголовка из accordance и содержат соответствующие таблицы.
4. Директории в `static/images` имеют название id заголовка из accordance и содержат соответствующие изображения.
5. В `static/text/reglaments-accordance` содержатся файлы имеющие название заголовка и хранящие в себе соответствующий глоссарий.
