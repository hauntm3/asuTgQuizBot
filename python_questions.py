from database import create_tables, SessionLocal, Question


def add_python_questions():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже вопросы по Python в базе
        existing_questions = (
            db.query(Question)
            .filter(
                Question.level.like("junior_python%")
                | Question.level.like("middle_python%")
                | Question.level.like("senior_python%")
            )
            .count()
        )

        if existing_questions > 0:
            print(
                f"В базе уже есть {existing_questions} вопросов по Python. Пропускаем добавление."
            )
            return

        # Если вопросов нет, добавляем их
        # Junior level questions
        junior_questions = [
            {
                "level": "junior_python",
                "question_text": "Что такое Python?",
                "option1": "Компилируемый язык программирования",
                "option2": "Интерпретируемый язык программирования высокого уровня",
                "option3": "Язык разметки",
                "option4": "Система управления базами данных",
                "correct_option": 2,
            },
            {
                "level": "junior_python",
                "question_text": "Как объявить список в Python?",
                "option1": "array = (1, 2, 3)",
                "option2": "array = {1, 2, 3}",
                "option3": "array = [1, 2, 3]",
                "option4": "array = <1, 2, 3>",
                "correct_option": 3,
            },
            {
                "level": "junior_python",
                "question_text": "Какой оператор используется для проверки типа переменной?",
                "option1": "typeof",
                "option2": "type()",
                "option3": "typecheck",
                "option4": "instanceof",
                "correct_option": 2,
            },
            {
                "level": "junior_python",
                "question_text": "Что такое PEP 8?",
                "option1": "Версия Python",
                "option2": "Руководство по стилю кода Python",
                "option3": "Библиотека Python",
                "option4": "Фреймворк для тестирования",
                "correct_option": 2,
            },
            {
                "level": "junior_python",
                "question_text": "Как создать виртуальное окружение в Python?",
                "option1": "python venv create",
                "option2": "virtualenv new",
                "option3": "python -m venv myenv",
                "option4": "pip install venv",
                "correct_option": 3,
            },
            {
                "level": "junior_python",
                "question_text": "Что делает оператор `//` в Python?",
                "option1": "Комментарий",
                "option2": "Целочисленное деление",
                "option3": "Возведение в степень",
                "option4": "Остаток от деления",
                "correct_option": 2,
            },
            {
                "level": "junior_python",
                "question_text": "Как получить длину строки в Python?",
                "option1": "str.length",
                "option2": "str.size()",
                "option3": "len(str)",
                "option4": "str.length()",
                "correct_option": 3,
            },
            {
                "level": "junior_python",
                "question_text": "Что такое индексация в Python?",
                "option1": "Способ создания переменных",
                "option2": "Метод сортировки данных",
                "option3": "Способ доступа к элементам последовательности",
                "option4": "Процесс компиляции кода",
                "correct_option": 3,
            },
            {
                "level": "junior_python",
                "question_text": "Какой тип данных используется для хранения уникальных элементов?",
                "option1": "list",
                "option2": "tuple",
                "option3": "dict",
                "option4": "set",
                "correct_option": 4,
            },
            {
                "level": "junior_python",
                "question_text": "Как объявить функцию в Python?",
                "option1": "function myFunc():",
                "option2": "def myFunc():",
                "option3": "new function myFunc():",
                "option4": "func myFunc():",
                "correct_option": 2,
            },
        ]

        # Дополнительные вопросы для junior уровня
        junior_questions.extend(
            [
                {
                    "level": "junior_python",
                    "question_text": "Что такое срезы (slices) в Python?",
                    "option1": "Способ разделить строку на части",
                    "option2": "Способ копирования списков",
                    "option3": "Способ получения подпоследовательности",
                    "option4": "Способ удаления элементов",
                    "correct_option": 3,
                },
                {
                    "level": "junior_python",
                    "question_text": "Как создать словарь в Python?",
                    "option1": "dict = {key: value}",
                    "option2": "dict = (key, value)",
                    "option3": "dict = [key, value]",
                    "option4": "dict = <key, value>",
                    "correct_option": 1,
                },
                {
                    "level": "junior_python",
                    "question_text": "Что делает оператор `is` в Python?",
                    "option1": "Сравнивает значения",
                    "option2": "Проверяет тип объекта",
                    "option3": "Проверяет идентичность объектов",
                    "option4": "Проверяет наличие атрибута",
                    "correct_option": 3,
                },
                {
                    "level": "junior_python",
                    "question_text": "Как добавить элемент в список?",
                    "option1": "list.add(item)",
                    "option2": "list.push(item)",
                    "option3": "list.insert(item)",
                    "option4": "list.append(item)",
                    "correct_option": 4,
                },
                {
                    "level": "junior_python",
                    "question_text": "Что такое f-строки в Python?",
                    "option1": "Форматированные строки",
                    "option2": "Функциональные строки",
                    "option3": "Фиксированные строки",
                    "option4": "Финальные строки",
                    "correct_option": 1,
                },
                {
                    "level": "junior_python",
                    "question_text": "Как перехватить исключение в Python?",
                    "option1": "catch Exception:",
                    "option2": "try-catch:",
                    "option3": "try-except:",
                    "option4": "handle Exception:",
                    "correct_option": 3,
                },
                {
                    "level": "junior_python",
                    "question_text": "Что делает метод strip()?",
                    "option1": "Разделяет строку на части",
                    "option2": "Удаляет пробелы в начале и конце",
                    "option3": "Соединяет строки",
                    "option4": "Заменяет символы",
                    "correct_option": 2,
                },
                {
                    "level": "junior_python",
                    "question_text": "Как объединить два списка?",
                    "option1": "list1 + list2",
                    "option2": "list1.join(list2)",
                    "option3": "list1.merge(list2)",
                    "option4": "list1.extend(list2)",
                    "correct_option": 1,
                },
                {
                    "level": "junior_python",
                    "question_text": "Что такое lambda-функция?",
                    "option1": "Многострочная функция",
                    "option2": "Рекурсивная функция",
                    "option3": "Анонимная однострочная функция",
                    "option4": "Функция высшего порядка",
                    "correct_option": 3,
                },
                {
                    "level": "junior_python",
                    "question_text": "Как получить ключи словаря?",
                    "option1": "dict.getKeys()",
                    "option2": "dict.keys()",
                    "option3": "dict.getkeys()",
                    "option4": "dict.key()",
                    "correct_option": 2,
                },
            ]
        )

        # Middle level questions
        middle_questions = [
            {
                "level": "middle_python",
                "question_text": "Что такое декоратор в Python?",
                "option1": "Функция для украшения кода",
                "option2": "Паттерн проектирования",
                "option3": "Функция, модифицирующая поведение другой функции",
                "option4": "Способ комментирования кода",
                "correct_option": 3,
            },
            {
                "level": "middle_python",
                "question_text": "Что такое генератор в Python?",
                "option1": "Функция, создающая случайные числа",
                "option2": "Функция, возвращающая итератор",
                "option3": "Класс для создания объектов",
                "option4": "Модуль для работы с файлами",
                "correct_option": 2,
            },
            {
                "level": "middle_python",
                "question_text": "Как работает сборщик мусора в Python?",
                "option1": "Подсчет ссылок и поиск циклических ссылок",
                "option2": "Ручное управление памятью",
                "option3": "Автоматическое удаление всех объектов",
                "option4": "Периодическая очистка памяти",
                "correct_option": 1,
            },
            {
                "level": "middle_python",
                "question_text": "Что такое контекстный менеджер?",
                "option1": "Менеджер процессов",
                "option2": "Класс для управления потоками",
                "option3": "Объект, реализующий __enter__ и __exit__",
                "option4": "Система управления памятью",
                "correct_option": 3,
            },
            {
                "level": "middle_python",
                "question_text": "Что такое asyncio?",
                "option1": "Библиотека для работы с базами данных",
                "option2": "Фреймворк для асинхронного программирования",
                "option3": "Модуль для работы с файлами",
                "option4": "Система тестирования",
                "correct_option": 2,
            },
            {
                "level": "middle_python",
                "question_text": "Что такое метакласс в Python?",
                "option1": "Класс, наследующий от object",
                "option2": "Класс, создающий другие классы",
                "option3": "Абстрактный класс",
                "option4": "Статический класс",
                "correct_option": 2,
            },
            {
                "level": "middle_python",
                "question_text": "Как работает GIL в Python?",
                "option1": "Позволяет выполнять много потоков одновременно",
                "option2": "Блокирует выполнение всех потоков",
                "option3": "Позволяет выполнять только один поток Python кода",
                "option4": "Управляет памятью в многопоточных программах",
                "correct_option": 3,
            },
            {
                "level": "middle_python",
                "question_text": "Что такое дескриптор в Python?",
                "option1": "Объект, определяющий поведение при доступе к атрибутам",
                "option2": "Способ описания классов",
                "option3": "Метод документирования кода",
                "option4": "Специальный комментарий",
                "correct_option": 1,
            },
            {
                "level": "middle_python",
                "question_text": "Как работает @property декоратор?",
                "option1": "Создает статический метод",
                "option2": "Делает метод приватным",
                "option3": "Превращает метод в атрибут",
                "option4": "Кэширует результат метода",
                "correct_option": 3,
            },
            {
                "level": "middle_python",
                "question_text": "Что такое MRO в Python?",
                "option1": "Способ оптимизации кода",
                "option2": "Порядок разрешения методов",
                "option3": "Система управления памятью",
                "option4": "Протокол обмена данными",
                "correct_option": 2,
            },
        ]

        # Дополнительные вопросы для middle уровня
        middle_questions.extend(
            [
                {
                    "level": "middle_python",
                    "question_text": "Что такое итератор в Python?",
                    "option1": "Объект, реализующий __iter__ и __next__",
                    "option2": "Объект для итерации по спискам",
                    "option3": "Функция для обхода коллекций",
                    "option4": "Специальный тип цикла",
                    "correct_option": 1,
                },
                {
                    "level": "middle_python",
                    "question_text": "Как работает @staticmethod?",
                    "option1": "Создает статическую переменную",
                    "option2": "Делает метод приватным",
                    "option3": "Позволяет вызывать метод без создания экземпляра",
                    "option4": "Кэширует результат метода",
                    "correct_option": 3,
                },
                {
                    "level": "middle_python",
                    "question_text": "Что такое множественное наследование?",
                    "option1": "Наследование от нескольких классов",
                    "option2": "Создание нескольких объектов",
                    "option3": "Наследование нескольких атрибутов",
                    "option4": "Копирование классов",
                    "correct_option": 1,
                },
                {
                    "level": "middle_python",
                    "question_text": "Как работает pickle в Python?",
                    "option1": "Шифрует данные",
                    "option2": "Сжимает файлы",
                    "option3": "Сериализует объекты Python",
                    "option4": "Форматирует код",
                    "correct_option": 3,
                },
                {
                    "level": "middle_python",
                    "question_text": "Что такое абстрактный класс?",
                    "option1": "Класс без методов",
                    "option2": "Класс, который нельзя инстанцировать",
                    "option3": "Класс без атрибутов",
                    "option4": "Приватный класс",
                    "correct_option": 2,
                },
                {
                    "level": "middle_python",
                    "question_text": "Как работает functools.partial?",
                    "option1": "Создает частично примененную функцию",
                    "option2": "Разделяет функцию на части",
                    "option3": "Объединяет функции",
                    "option4": "Кэширует функцию",
                    "correct_option": 1,
                },
                {
                    "level": "middle_python",
                    "question_text": "Что такое корутины в Python?",
                    "option1": "Функции для работы с потоками",
                    "option2": "Подпрограммы для рекурсии",
                    "option3": "Функции с возможностью приостановки",
                    "option4": "Обработчики исключений",
                    "correct_option": 3,
                },
                {
                    "level": "middle_python",
                    "question_text": "Как работает collections.defaultdict?",
                    "option1": "Создает неизменяемый словарь",
                    "option2": "Создает словарь с значением по умолчанию",
                    "option3": "Сортирует словарь",
                    "option4": "Объединяет словари",
                    "correct_option": 2,
                },
                {
                    "level": "middle_python",
                    "question_text": "Что такое метод __call__?",
                    "option1": "Метод для вызова объекта как функции",
                    "option2": "Метод инициализации",
                    "option3": "Метод удаления объекта",
                    "option4": "Метод сравнения объектов",
                    "correct_option": 1,
                },
                {
                    "level": "middle_python",
                    "question_text": "Как работает threading.Lock?",
                    "option1": "Блокирует файлы",
                    "option2": "Блокирует доступ к базе данных",
                    "option3": "Обеспечивает синхронизацию потоков",
                    "option4": "Блокирует сетевые соединения",
                    "correct_option": 3,
                },
            ]
        )

        # Senior level questions
        senior_questions = [
            {
                "level": "senior_python",
                "question_text": "Что такое модуль Cython?",
                "option1": "Версия Python для Windows",
                "option2": "Компилятор Python в C",
                "option3": "Фреймворк для веб-разработки",
                "option4": "Система управления пакетами",
                "correct_option": 2,
            },
            {
                "level": "senior_python",
                "question_text": "Как работает PyPy?",
                "option1": "Компилирует Python в машинный код",
                "option2": "Интерпретирует Python код",
                "option3": "JIT-компиляция Python кода",
                "option4": "Оптимизирует память",
                "correct_option": 3,
            },
            {
                "level": "senior_python",
                "question_text": "Что такое профилирование в Python?",
                "option1": "Анализ производительности кода",
                "option2": "Создание профилей пользователей",
                "option3": "Настройка окружения",
                "option4": "Тестирование кода",
                "correct_option": 1,
            },
            {
                "level": "senior_python",
                "question_text": "Как работает uvicorn?",
                "option1": "Веб-фреймворк",
                "option2": "ASGI сервер реализации",
                "option3": "ORM для баз данных",
                "option4": "Система кэширования",
                "correct_option": 2,
            },
            {
                "level": "senior_python",
                "question_text": "Что такое Celery?",
                "option1": "Библиотека для работы с датами",
                "option2": "Система управления базами данных",
                "option3": "Распределенная очередь задач",
                "option4": "Фреймворк для тестирования",
                "correct_option": 3,
            },
            {
                "level": "senior_python",
                "question_text": "Как работает механизм slots в Python?",
                "option1": "Ограничивает атрибуты класса",
                "option2": "Создает слоты для многопоточности",
                "option3": "Управляет памятью",
                "option4": "Оптимизирует вызовы методов",
                "correct_option": 1,
            },
            {
                "level": "senior_python",
                "question_text": "Что такое GraphQL в Python?",
                "option1": "Библиотека для работы с графами",
                "option2": "Язык запросов для API",
                "option3": "Система визуализации данных",
                "option4": "Фреймворк для машинного обучения",
                "correct_option": 2,
            },
            {
                "level": "senior_python",
                "question_text": "Как работает FastAPI?",
                "option1": "На основе WSGI",
                "option2": "На основе Django",
                "option3": "На основе ASGI и Starlette",
                "option4": "На основе Flask",
                "correct_option": 3,
            },
            {
                "level": "senior_python",
                "question_text": "Что такое Docker Compose?",
                "option1": "Система контейнеризации",
                "option2": "Инструмент для оркестрации контейнеров",
                "option3": "Система мониторинга",
                "option4": "База данных",
                "correct_option": 2,
            },
            {
                "level": "senior_python",
                "question_text": "Как работает asyncpg?",
                "option1": "Синхронный драйвер PostgreSQL",
                "option2": "ORM для MongoDB",
                "option3": "Асинхронный драйвер PostgreSQL",
                "option4": "Система кэширования",
                "correct_option": 3,
            },
        ]

        # Дополнительные вопросы для senior уровня
        senior_questions.extend(
            [
                {
                    "level": "senior_python",
                    "question_text": "Что такое метапрограммирование?",
                    "option1": "Программирование на низком уровне",
                    "option2": "Программирование, создающее или модифицирующее код",
                    "option3": "Программирование микроконтроллеров",
                    "option4": "Программирование баз данных",
                    "correct_option": 2,
                },
                {
                    "level": "senior_python",
                    "question_text": "Как работает asyncio.gather?",
                    "option1": "Собирает результаты асинхронных задач",
                    "option2": "Объединяет потоки",
                    "option3": "Группирует данные",
                    "option4": "Собирает статистику",
                    "correct_option": 1,
                },
                {
                    "level": "senior_python",
                    "question_text": "Что такое Django ORM?",
                    "option1": "Система шаблонов",
                    "option2": "Маршрутизатор URL",
                    "option3": "Объектно-реляционное отображение",
                    "option4": "Система кэширования",
                    "correct_option": 3,
                },
                {
                    "level": "senior_python",
                    "question_text": "Как работает SQLAlchemy?",
                    "option1": "Как простой SQL клиент",
                    "option2": "Как ORM и SQL инструментарий",
                    "option3": "Как система миграций",
                    "option4": "Как кэш для SQL запросов",
                    "correct_option": 2,
                },
                {
                    "level": "senior_python",
                    "question_text": "Что такое Dependency Injection?",
                    "option1": "Внедрение зависимостей",
                    "option2": "Установка пакетов",
                    "option3": "Внедрение кода",
                    "option4": "Связывание модулей",
                    "correct_option": 1,
                },
                {
                    "level": "senior_python",
                    "question_text": "Как работает pytest?",
                    "option1": "Как система сборки",
                    "option2": "Как отладчик",
                    "option3": "Как фреймворк для тестирования",
                    "option4": "Как профилировщик",
                    "correct_option": 3,
                },
                {
                    "level": "senior_python",
                    "question_text": "Что такое RabbitMQ?",
                    "option1": "База данных",
                    "option2": "Брокер сообщений",
                    "option3": "Web-сервер",
                    "option4": "ORM",
                    "correct_option": 2,
                },
                {
                    "level": "senior_python",
                    "question_text": "Как работает Gunicorn?",
                    "option1": "WSGI HTTP сервер",
                    "option2": "Система кэширования",
                    "option3": "Балансировщик нагрузки",
                    "option4": "Прокси-сервер",
                    "correct_option": 1,
                },
                {
                    "level": "senior_python",
                    "question_text": "Что такое Apache Airflow?",
                    "option1": "Web-сервер",
                    "option2": "Система мониторинга",
                    "option3": "Платформа для оркестрации рабочих процессов",
                    "option4": "Система логирования",
                    "correct_option": 3,
                },
                {
                    "level": "senior_python",
                    "question_text": "Как работает Redis с Python?",
                    "option1": "Как SQL база данных",
                    "option2": "Как key-value хранилище в памяти",
                    "option3": "Как файловое хранилище",
                    "option4": "Как брокер сообщений",
                    "correct_option": 2,
                },
            ]
        )

        # Добавляем вопросы в базу данных
        all_questions = junior_questions + middle_questions + senior_questions
        for q in all_questions:
            question = Question(**q)
            db.add(question)

        db.commit()
        print("Python вопросы успешно добавлены в базу данных!")

    finally:
        db.close()


if __name__ == "__main__":
    add_python_questions()
