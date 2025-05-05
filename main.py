from database import create_tables
from java_questions import add_java_questions
from python_questions import add_python_questions
from sql_questions import add_sql_questions

if __name__ == "__main__":
    # Создаем таблицы (обязательно!)
    create_tables()

    # Добавляем вопросы (если их нет в БД)
    add_java_questions()
    add_python_questions()
    add_sql_questions()

    # Импортируем и запускаем бота только после создания таблиц
    from bot import main

    main()
