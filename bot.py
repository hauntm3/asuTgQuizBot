import logging
import asyncio
import random
import os
from contextlib import contextmanager
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from database import create_tables, get_db, Question, UserProgress, UserStats
from sqlalchemy import select, desc, func
from datetime import datetime

# Импортируем все необходимое из custom_tests
from custom_tests import (
    start_test_creation,
    ask_test_name,
    ask_question,
    ask_option_1,
    ask_option_2,
    ask_option_3,
    ask_option_4,
    ask_correct_option,
    confirm_add_question,
    cancel_creation,
    show_test_catalog,
    # Состояния
    ASK_TEST_NAME,
    ASK_QUESTION,
    ASK_OPTION_1,
    ASK_OPTION_2,
    ASK_OPTION_3,
    ASK_OPTION_4,
    ASK_CORRECT_OPTION,
    CONFIRM_ADD_QUESTION,
    # Добавляем run_custom_test
    run_custom_test,
    # Добавляем handle_custom_answer
    handle_custom_answer,
)

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Получение токена из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")

# Константы
LANGUAGE_DISPLAY = {"python": "Python", "sql": "SQL", "java": "Java"}


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message=None):
    keyboard = [
        [InlineKeyboardButton("🎯 Начать тестирование", callback_data="start_test")],
        [InlineKeyboardButton("📝 Создать свой тест", callback_data="create_test")],
        [InlineKeyboardButton("📚 Каталог тестов", callback_data="test_catalog")],
        [InlineKeyboardButton("📊 Таблица лидеров", callback_data="leaderboard")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = message or (
        "🎯 Добро пожаловать в Quiz Bot!\n\n"
        "Здесь вы можете проверить свои знания Java, Python и SQL на разных уровнях сложности.\n"
        "Выберите действие из меню ниже:"
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=text, reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await main_menu(update, context)


async def show_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Java", callback_data="lang_java")],
        [InlineKeyboardButton("Python", callback_data="lang_python")],
        [InlineKeyboardButton("SQL", callback_data="lang_sql")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        "Выберите язык программирования:", reply_markup=reply_markup
    )


async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Сохраняем выбранный язык в контексте пользователя
    context.user_data["selected_language"] = query.data.split("_")[1]

    # Показываем уровни сложности для выбранного языка
    await show_difficulty_levels(update, context)


async def show_difficulty_levels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_language = context.user_data.get("selected_language", "java")
    lang_prefix = LANGUAGE_DISPLAY.get(selected_language, "Java")

    keyboard = [
        [
            InlineKeyboardButton(
                f"👶 {lang_prefix} Junior",
                callback_data=f"level_{selected_language}_junior",
            )
        ],
        [
            InlineKeyboardButton(
                f"👨‍💻 {lang_prefix} Middle",
                callback_data=f"level_{selected_language}_middle",
            )
        ],
        [
            InlineKeyboardButton(
                f"🧙‍♂️ {lang_prefix} Senior",
                callback_data=f"level_{selected_language}_senior",
            )
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="start_test")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        f"Выберите уровень сложности для {lang_prefix}:", reply_markup=reply_markup
    )


async def handle_level_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Получаем язык и уровень из callback_data
    _, language, level = query.data.split("_")
    user_id = query.from_user.id
    username = query.from_user.username or f"User{user_id}"
    level_key = f"{level}_{language}"

    with get_db() as db:
        # Очищаем предыдущий прогресс
        db.query(UserProgress).filter(UserProgress.user_id == user_id).delete()

        # Получаем все вопросы для выбранного языка и уровня
        questions = db.query(Question).filter(Question.level == level_key).all()

        # Выбираем 10 случайных вопросов
        selected_questions = random.sample(questions, min(10, len(questions)))
        selected_question_ids = [q.id for q in selected_questions]

        # Создаем новый прогресс с выбранными вопросами
        progress = UserProgress(
            user_id=user_id,
            level=level_key,
            is_testing=True,
            question_ids=",".join(map(str, selected_question_ids)),
        )
        db.add(progress)

        # Создаем или обновляем статистику пользователя
        stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
        if not stats:
            stats = UserStats(user_id=user_id, username=username)
            db.add(stats)

        db.commit()

    lang_name = LANGUAGE_DISPLAY.get(language, "Java")

    await query.edit_message_text(
        f"📚 Вы выбрали {lang_name}, уровень: {level.capitalize()}\n"
        "Начинаем тестирование! Удачи! 🍀\n\n"
        "Всего будет 10 вопросов. На каждый вопрос дается 4 варианта ответа."
    )

    # Отправляем первый вопрос
    await send_question(update, context, user_id)


async def get_question_message(question, progress):
    """Форматирует сообщение с вопросом"""
    return (
        f"❓ Вопрос {progress.current_question + 1}/10:\n\n"
        f"{question.question_text}\n\n"
        f"Варианты ответов:\n"
        f"1️⃣ {question.option1}\n"
        f"2️⃣ {question.option2}\n"
        f"3️⃣ {question.option3}\n"
        f"4️⃣ {question.option4}"
    )


async def send_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int
):
    with get_db() as db:
        progress = (
            db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        )
        if not progress or not progress.is_testing:
            return

        # Получаем список ID выбранных вопросов
        question_ids = list(map(int, progress.question_ids.split(",")))
        if progress.current_question >= len(question_ids):
            # Тест завершен
            await finish_test(update, context, user_id, progress.correct_answers)
            return

        # Получаем текущий вопрос по его ID
        current_question_id = question_ids[progress.current_question]
        question = db.query(Question).filter(Question.id == current_question_id).first()

        # Создаем текст сообщения с вопросом
        message_text = await get_question_message(question, progress)

        # Создаем кнопки с номерами
        keyboard = [
            [
                InlineKeyboardButton("1️⃣", callback_data="answer_1"),
                InlineKeyboardButton("2️⃣", callback_data="answer_2"),
                InlineKeyboardButton("3️⃣", callback_data="answer_3"),
                InlineKeyboardButton("4️⃣", callback_data="answer_4"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем новое сообщение с вопросом
        await context.bot.send_message(
            chat_id=user_id, text=message_text, reply_markup=reply_markup
        )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    selected_option = int(query.data.split("_")[1])

    with get_db() as db:
        progress = (
            db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        )
        if not progress or not progress.is_testing:
            return

        # Получаем список ID выбранных вопросов
        question_ids = list(map(int, progress.question_ids.split(",")))
        # Получаем текущий вопрос по его ID
        current_question_id = question_ids[progress.current_question]
        question = db.query(Question).filter(Question.id == current_question_id).first()

        # Проверяем правильность ответа
        is_correct = question.correct_option == selected_option
        correct_answer_text = getattr(question, f"option{question.correct_option}")
        selected_answer_text = getattr(question, f"option{selected_option}")

        # Сохраняем текст вопроса для отображения
        question_text = await get_question_message(question, progress)

        if is_correct:
            progress.correct_answers += 1
            feedback = (
                f"{question_text}\n\n"
                "✅ Правильно!\n\n"
                f"Ваш ответ: {selected_answer_text}"
            )
        else:
            feedback = (
                f"{question_text}\n\n"
                "❌ Неправильно!\n\n"
                f"Ваш ответ: {selected_answer_text}\n"
                f"Правильный ответ: {correct_answer_text}"
            )

        progress.current_question += 1
        progress.last_answer_time = datetime.utcnow()
        db.commit()

    # Обновляем текущее сообщение, убирая кнопки и показывая результат
    await query.edit_message_text(text=feedback)

    # Отправляем следующий вопрос в новом сообщении
    await send_question(update, context, user_id)


async def finish_test(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    correct_answers: int,
):
    # Объявляем переменные за пределами контекстного менеджера
    level = ""
    mmr_change = 0
    old_mmr = 0
    new_mmr = 0

    with get_db() as db:
        progress = (
            db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        )
        if not progress:
            return

        level = progress.level
        progress.is_testing = False

        # Обновляем статистику пользователя
        stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
        if stats:
            # Рассчитываем изменение MMR
            mmr_change = stats.calculate_mmr_change(correct_answers, level)
            old_mmr = stats.mmr
            stats.mmr = max(
                0, stats.mmr + mmr_change
            )  # MMR не может быть отрицательным
            new_mmr = stats.mmr  # Сохраняем новый MMR в локальную переменную
            stats.total_tests += 1
            stats.last_test_date = datetime.utcnow()

        db.commit()

    percentage = (correct_answers / 10) * 100

    # Оценка результата
    if percentage >= 90:
        grade = "🏆 Превосходно! Вы настоящий профессионал!"
    elif percentage >= 70:
        grade = "👍 Хороший результат! Есть небольшие пробелы в знаниях."
    elif percentage >= 50:
        grade = "📚 Вам стоит больше практиковаться."
    else:
        grade = "💪 Не отчаивайтесь, продолжайте учиться!"

    # Получаем базовый уровень для отображения
    display_level = level.split("_")[0] if "_" in level else level

    # Добавляем информацию об изменении MMR
    mmr_text = "🔺" if mmr_change > 0 else "🔻" if mmr_change < 0 else "➖"
    stats_text = (
        f"\n\nРезультаты теста:\n"
        f"Уровень: {display_level.capitalize()}\n"
        f"Правильных ответов: {correct_answers}/10 ({percentage:.1f}%)\n"
        f"MMR: {old_mmr} {mmr_text} {abs(mmr_change)} = {new_mmr}\n"
    )

    # Сначала отправляем сообщение с результатами без кнопок
    try:
        await context.bot.send_message(
            chat_id=user_id, text=f"🎯 Результат теста:\n\n{grade}{stats_text}"
        )
    except Exception as e:
        logging.error(f"Ошибка при отображении результатов: {e}")

    # Затем отправляем новое сообщение с кнопками навигации
    keyboard = [
        [InlineKeyboardButton("🔄 Пройти тест снова", callback_data="start_test")],
        [InlineKeyboardButton("📊 Таблица лидеров", callback_data="leaderboard")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=user_id, text="Выберите дальнейшее действие:", reply_markup=reply_markup
    )


async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with get_db() as db:
        # Получаем топ-5 пользователей по MMR
        top_users = (
            db.query(UserStats)
            .filter(UserStats.total_tests > 0)
            .order_by(desc(UserStats.mmr))
            .limit(5)
            .all()
        )

    text = "🏆 Таблица лидеров\n\n"
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    ranks = ["Грандмастер", "Мастер", "Эксперт", "Специалист", "Новичок"]

    for i, user in enumerate(top_users):
        medal = medals[i]
        rank = ranks[i] if user.mmr >= 1000 else "Новичок"
        username = user.username or f"User{user.user_id}"

        # Добавляем звездочки в зависимости от MMR
        stars = "⭐" * (user.mmr // 200)  # 1 звезда за каждые 200 MMR

        text += (
            f"{medal} {username}\n"
            f"    {stars}\n"
            f"    Ранг: {rank}\n"
            f"    MMR: {user.mmr}\n"
            f"    Тестов пройдено: {user.total_tests}\n\n"
        )

    if not top_users:
        text += "😢 Пока никто не прошел ни одного теста\n"
        text += "🎯 Станьте первым в рейтинге!\n"

    keyboard = [
        [InlineKeyboardButton("🔄 Пройти тест", callback_data="start_test")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ Помощь по использованию бота:\n\n"
        "1. Начало тестирования:\n"
        "   • Нажмите '🎯 Начать тестирование'\n"
        "   • Выберите язык (Java, Python или SQL)\n"
        "   • Выберите уровень сложности\n"
        "   • Ответьте на 10 вопросов\n\n"
        "2. Уровни сложности для каждого языка:\n"
        "   👶 Junior - базовые концепции\n"
        "   👨‍💻 Middle - продвинутые темы\n"
        "   🧙‍♂️ Senior - архитектура и паттерны\n\n"
        "3. Навигация:\n"
        "   • Кнопка '🏠 Главное меню' доступна везде(кроме процесса тестирования)\n"
        "   • Можно прервать тест в любой момент\n\n"
        "Удачи в изучении программирования! 🚀"
    )

    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)


def setup_handlers(application):
    """Настройка обработчиков сообщений"""
    # Обработчик диалога для создания теста
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_test_creation, pattern="^create_test$")
        ],
        states={
            ASK_TEST_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_test_name)
            ],
            ASK_QUESTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_question)
            ],
            ASK_OPTION_1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_option_1)
            ],
            ASK_OPTION_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_option_2)
            ],
            ASK_OPTION_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_option_3)
            ],
            ASK_OPTION_4: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_option_4)
            ],
            ASK_CORRECT_OPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_correct_option)
            ],
            CONFIRM_ADD_QUESTION: [
                CallbackQueryHandler(
                    confirm_add_question, pattern="^(add_another_q|finish_creation)$"
                )
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_creation)],
        per_message=False,  # Используем один обработчик на пользователя
    )

    application.add_handler(conv_handler)  # Добавляем обработчик диалога

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        CallbackQueryHandler(show_language_selection, pattern="^start_test$")
    )
    application.add_handler(
        CallbackQueryHandler(handle_language_selection, pattern="^lang_")
    )
    application.add_handler(
        CallbackQueryHandler(handle_level_selection, pattern="^level_")
    )
    application.add_handler(CallbackQueryHandler(handle_answer, pattern="^answer_"))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    application.add_handler(
        CallbackQueryHandler(show_leaderboard, pattern="^leaderboard$")
    )
    application.add_handler(CallbackQueryHandler(show_help, pattern="^help$"))
    application.add_handler(
        CallbackQueryHandler(show_test_catalog, pattern="^test_catalog(?:_\d+)?$")
    )  # Добавляем обработчик каталога
    # Добавляем обработчик для запуска кастомного теста
    application.add_handler(
        CallbackQueryHandler(run_custom_test, pattern="^run_custom_")
    )
    # Добавляем обработчик для ответов на кастомный тест
    application.add_handler(
        CallbackQueryHandler(handle_custom_answer, pattern="^custom_answer_")
    )


def main():
    # Создаем таблицы базы данных
    create_tables()

    # Инициализируем бота
    application = Application.builder().token(TOKEN).build()

    # Настраиваем обработчики
    setup_handlers(application)

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
