from database import create_tables, SessionLocal, Question


def add_sql_questions():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже вопросы по SQL в базе
        existing_questions = (
            db.query(Question)
            .filter(
                Question.level.like("junior_sql%")
                | Question.level.like("middle_sql%")
                | Question.level.like("senior_sql%")
            )
            .count()
        )

        if existing_questions > 0:
            print(
                f"В базе уже есть {existing_questions} вопросов по SQL. Пропускаем добавление."
            )
            return

        # Если вопросов нет, добавляем их
        # Junior level questions
        junior_questions = [
            {
                "level": "junior_sql",
                "question_text": "Что такое SQL?",
                "option1": "Структурированный язык моделирования",
                "option2": "Язык структурированных запросов",
                "option3": "Система управления серверами",
                "option4": "Программный интерфейс для работы с сетью",
                "correct_option": 2,
            },
            {
                "level": "junior_sql",
                "question_text": "Какой оператор используется для извлечения данных из таблицы?",
                "option1": "UPDATE",
                "option2": "INSERT",
                "option3": "DELETE",
                "option4": "SELECT",
                "correct_option": 4,
            },
            {
                "level": "junior_sql",
                "question_text": "Какой оператор используется для объединения строк из двух или более таблиц?",
                "option1": "JOIN",
                "option2": "MERGE",
                "option3": "CONNECT",
                "option4": "UNION",
                "correct_option": 1,
            },
            {
                "level": "junior_sql",
                "question_text": "Какой оператор используется для вставки новых данных в таблицу?",
                "option1": "INSERT INTO",
                "option2": "ADD",
                "option3": "UPDATE",
                "option4": "CREATE",
                "correct_option": 1,
            },
            {
                "level": "junior_sql",
                "question_text": "Как удалить данные из таблицы?",
                "option1": "REMOVE FROM",
                "option2": "DELETE FROM",
                "option3": "DROP TABLE",
                "option4": "CLEAR TABLE",
                "correct_option": 2,
            },
            {
                "level": "junior_sql",
                "question_text": "Какой оператор используется для фильтрации результатов в SQL?",
                "option1": "FILTER",
                "option2": "HAVING",
                "option3": "WHERE",
                "option4": "CONDITION",
                "correct_option": 3,
            },
            {
                "level": "junior_sql",
                "question_text": "Какой оператор используется для сортировки результатов запроса?",
                "option1": "SORT BY",
                "option2": "ORDER BY",
                "option3": "ARRANGE BY",
                "option4": "GROUP BY",
                "correct_option": 2,
            },
            {
                "level": "junior_sql",
                "question_text": "Какой тип данных используется для хранения целых чисел в SQL?",
                "option1": "FLOAT",
                "option2": "CHAR",
                "option3": "INT",
                "option4": "TEXT",
                "correct_option": 3,
            },
            {
                "level": "junior_sql",
                "question_text": "Какой оператор используется для группировки строк с одинаковыми значениями?",
                "option1": "GROUP BY",
                "option2": "ORDER BY",
                "option3": "SORT BY",
                "option4": "CLUSTER BY",
                "correct_option": 1,
            },
            {
                "level": "junior_sql",
                "question_text": "Что такое PRIMARY KEY?",
                "option1": "Первый столбец в таблице",
                "option2": "Уникальный идентификатор каждой строки в таблице",
                "option3": "Основная таблица в базе данных",
                "option4": "Пароль для доступа к базе данных",
                "correct_option": 2,
            },
        ]

        # Middle level questions
        middle_questions = [
            {
                "level": "middle_sql",
                "question_text": "Что такое нормализация базы данных?",
                "option1": "Оптимизация запросов для более быстрого выполнения",
                "option2": "Процесс организации данных для минимизации избыточности",
                "option3": "Резервное копирование данных",
                "option4": "Процесс индексирования таблиц",
                "correct_option": 2,
            },
            {
                "level": "middle_sql",
                "question_text": "Какой тип JOIN возвращает строки, когда есть совпадение в обеих таблицах?",
                "option1": "LEFT JOIN",
                "option2": "RIGHT JOIN",
                "option3": "INNER JOIN",
                "option4": "FULL JOIN",
                "correct_option": 3,
            },
            {
                "level": "middle_sql",
                "question_text": "Что такое индекс в базе данных?",
                "option1": "Структура данных для ускорения поиска записей",
                "option2": "Список всех таблиц в базе данных",
                "option3": "Метод шифрования данных",
                "option4": "Первичный ключ таблицы",
                "correct_option": 1,
            },
            {
                "level": "middle_sql",
                "question_text": "Что означает аббревиатура ACID в контексте баз данных?",
                "option1": "Advanced Control Interface Design",
                "option2": "Atomicity, Consistency, Isolation, Durability",
                "option3": "Automatic Column Index Definition",
                "option4": "Asynchronous Connection Integration Driver",
                "correct_option": 2,
            },
            {
                "level": "middle_sql",
                "question_text": "Что такое foreign key (внешний ключ)?",
                "option1": "Ключ от другой базы данных",
                "option2": "Поле, связывающее таблицу с другой таблицей",
                "option3": "Резервная копия первичного ключа",
                "option4": "Ключ шифрования данных",
                "correct_option": 2,
            },
            {
                "level": "middle_sql",
                "question_text": "Что такое SQL инъекция?",
                "option1": "Техника оптимизации SQL запросов",
                "option2": "Автоматическое добавление данных в таблицу",
                "option3": "Метод атаки, при котором вредоносный код внедряется в SQL-запрос",
                "option4": "Способ передачи данных между таблицами",
                "correct_option": 3,
            },
            {
                "level": "middle_sql",
                "question_text": "Что делает команда TRUNCATE TABLE?",
                "option1": "Удаляет таблицу из базы данных",
                "option2": "Удаляет все строки из таблицы, но сохраняет структуру",
                "option3": "Удаляет указанную колонку из таблицы",
                "option4": "Изменяет структуру таблицы",
                "correct_option": 2,
            },
            {
                "level": "middle_sql",
                "question_text": "Что такое представление (view) в SQL?",
                "option1": "Графический интерфейс для работы с базой данных",
                "option2": "Виртуальная таблица, основанная на результате SQL запроса",
                "option3": "Способ отображения схемы базы данных",
                "option4": "Отчет о производительности запросов",
                "correct_option": 2,
            },
            {
                "level": "middle_sql",
                "question_text": "Какая разница между LEFT JOIN и RIGHT JOIN?",
                "option1": "LEFT JOIN работает быстрее, чем RIGHT JOIN",
                "option2": "LEFT JOIN возвращает все строки из левой таблицы, RIGHT JOIN - из правой",
                "option3": "LEFT JOIN применяется только для таблиц с первичными ключами",
                "option4": "Нет разницы, это просто разные названия одной операции",
                "correct_option": 2,
            },
            {
                "level": "middle_sql",
                "question_text": "Что такое денормализация базы данных?",
                "option1": "Исправление ошибок в структуре базы данных",
                "option2": "Процесс добавления избыточности для улучшения производительности чтения",
                "option3": "Восстановление базы данных после сбоя",
                "option4": "Преобразование реляционной базы данных в нереляционную",
                "correct_option": 2,
            },
        ]

        # Senior level questions
        senior_questions = [
            {
                "level": "senior_sql",
                "question_text": "Что такое транзакция в базе данных?",
                "option1": "Перенос данных между таблицами",
                "option2": "Единица работы, которая обрабатывается атомарно",
                "option3": "Метод резервного копирования",
                "option4": "Тип соединения таблиц",
                "correct_option": 2,
            },
            {
                "level": "senior_sql",
                "question_text": "Что такое подзапрос (subquery)?",
                "option1": "Тип хранимой процедуры",
                "option2": "Запрос внутри другого запроса",
                "option3": "Запрос, выполняемый после основного",
                "option4": "Функция агрегации данных",
                "correct_option": 2,
            },
            {
                "level": "senior_sql",
                "question_text": "Что делает оператор HAVING?",
                "option1": "Фильтрует строки после группировки",
                "option2": "Фильтрует строки перед группировкой",
                "option3": "Объединяет результаты нескольких запросов",
                "option4": "Сортирует результат запроса",
                "correct_option": 1,
            },
            {
                "level": "senior_sql",
                "question_text": "Что такое materialized view?",
                "option1": "Другое название для таблицы",
                "option2": "Сохраненная физическая копия результата запроса",
                "option3": "Временная таблица",
                "option4": "Виртуальная таблица, обновляемая в реальном времени",
                "correct_option": 2,
            },
            {
                "level": "senior_sql",
                "question_text": "Что такое оконные функции в SQL?",
                "option1": "Функции для работы с графическим интерфейсом",
                "option2": "Функции, позволяющие выполнять вычисления над набором строк, связанных с текущей строкой",
                "option3": "Функции, ограниченные временным окном выполнения",
                "option4": "Функции для работы с операционной системой",
                "correct_option": 2,
            },
            {
                "level": "senior_sql",
                "question_text": "Что такое секционирование (partitioning) таблиц?",
                "option1": "Разделение таблицы на несколько логических частей",
                "option2": "Распределение таблицы по разным базам данных",
                "option3": "Группировка таблиц по категориям",
                "option4": "Шифрование частей таблицы",
                "correct_option": 1,
            },
            {
                "level": "senior_sql",
                "question_text": "Что такое хранимая процедура?",
                "option1": "SQL запрос, сохраненный в базе данных для многократного использования",
                "option2": "Механизм резервного копирования",
                "option3": "Специальный тип индекса",
                "option4": "Метод шифрования данных",
                "correct_option": 1,
            },
            {
                "level": "senior_sql",
                "question_text": "Что такое план выполнения запроса (execution plan)?",
                "option1": "Документация по SQL запросам",
                "option2": "Последовательность шагов, выполняемых СУБД при обработке SQL запроса",
                "option3": "План разработки базы данных",
                "option4": "График обновления данных",
                "correct_option": 2,
            },
            {
                "level": "senior_sql",
                "question_text": "Что такое deadlock в базах данных?",
                "option1": "Ситуация, когда база данных достигает максимального размера",
                "option2": "Ситуация, когда две транзакции блокируют друг друга, ожидая освобождения ресурсов",
                "option3": "Неиспользуемая таблица в базе данных",
                "option4": "Ошибка в структуре таблицы",
                "correct_option": 2,
            },
            {
                "level": "senior_sql",
                "question_text": "Что такое курсор в SQL?",
                "option1": "Указатель на текущую позицию в результате запроса",
                "option2": "Инструмент для ввода SQL команд",
                "option3": "Тип данных для хранения координат",
                "option4": "Специальный символ в SQL синтаксисе",
                "correct_option": 1,
            },
        ]

        # Добавляем вопросы в базу данных
        all_questions = junior_questions + middle_questions + senior_questions
        for q in all_questions:
            question = Question(**q)
            db.add(question)

        db.commit()
        print("SQL вопросы успешно добавлены в базу данных!")

    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
    add_sql_questions()
