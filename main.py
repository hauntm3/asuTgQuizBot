from database import create_tables
from java_questions import add_java_questions
from python_questions import add_python_questions
from sql_questions import add_sql_questions
from bot import main

if __name__ == "__main__":
    # Создаем таблицы и добавляем вопросы
    create_tables()
    add_java_questions()
    add_python_questions()
    add_sql_questions()

    # Запускаем бота
    main()
