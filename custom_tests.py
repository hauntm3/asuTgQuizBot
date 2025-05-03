import logging
from telegram import (
    Update,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler
import json
import os
from datetime import datetime

# Импортируем get_db_session и UserStats из database.py
from database import get_db, UserStats

# Импортируем main_menu из bot.py
# Это может создать цикл импорта, если bot.py тоже импортирует что-то из custom_tests.py
# Если возникнут проблемы, нужно будет рефакторить.
# from bot import main_menu # Убираем импорт отсюда

# Состояния для диалога создания теста
(
    ASK_TEST_NAME,
    ASK_QUESTION,
    ASK_OPTION_1,
    ASK_OPTION_2,
    ASK_OPTION_3,
    ASK_OPTION_4,
    ASK_CORRECT_OPTION,
    CONFIRM_ADD_QUESTION,
    FINISH_TEST_CREATION,
) = range(9)

# Путь к файлу для хранения кастомных тестов
CUSTOM_TESTS_FILE = "asuTgQuizBot/custom_tests.json"
TESTS_PER_PAGE = 5  # Количество тестов на одной странице каталога

# --- Функции для работы с хранилищем тестов ---


def load_custom_tests():
    if not os.path.exists(CUSTOM_TESTS_FILE):
        return {}
    try:
        with open(CUSTOM_TESTS_FILE, "r", encoding="utf-8") as f:
            # Загружаем данные, преобразуя ключи (user_id) из строк в int
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}  # Возвращаем пустой словарь, если файл пуст, не найден или поврежден


def save_custom_tests(tests_data):
    with open(CUSTOM_TESTS_FILE, "w", encoding="utf-8") as f:
        # Сохраняем данные, ключи (user_id) остаются int, json их преобразует в строки
        json.dump(tests_data, f, ensure_ascii=False, indent=4)


# Глобальный словарь для хранения всех кастомных тестов (user_id -> list of tests)
# Загружаем тесты при старте
custom_tests_storage = load_custom_tests()


# --- Обработчики для ConversationHandler ---


async def start_test_creation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Начинает процесс создания нового теста, запрашивает название."""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Отлично! Давайте создадим новый тест. \n\n📝 Введите название вашего теста:"
    )
    # Инициализируем данные для нового теста в user_data
    context.user_data["new_test"] = {"name": None, "questions": []}
    return ASK_TEST_NAME


async def ask_test_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает введенное название теста и запрашивает первый вопрос."""
    test_name = update.message.text
    if not test_name or len(test_name) < 3:
        await update.message.reply_text(
            "Название теста должно быть не менее 3 символов. Попробуйте еще раз:"
        )
        return ASK_TEST_NAME

    context.user_data["new_test"]["name"] = test_name
    # Очищаем данные для нового вопроса
    context.user_data["current_question"] = {}
    await update.message.reply_text(
        f"Название теста '{test_name}' принято.\n\n"
        "Теперь введите текст первого вопроса:"
    )
    return ASK_QUESTION


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет текст предыдущего вопроса (если он был) и запрашивает текст варианта 1."""
    question_text = update.message.text
    if not question_text or len(question_text) < 5:
        await update.message.reply_text(
            "Текст вопроса должен быть не менее 5 символов. Введите еще раз:"
        )
        return ASK_QUESTION  # Остаемся в том же состоянии

    context.user_data["current_question"]["text"] = question_text
    await update.message.reply_text(
        "Вопрос принят. Теперь введите текст для первого варианта ответа (1️⃣):"
    )
    return ASK_OPTION_1


async def ask_option_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет вариант 1 и запрашивает вариант 2."""
    option1_text = update.message.text
    if not option1_text:
        await update.message.reply_text(
            "Вариант ответа не может быть пустым. Введите текст для варианта 1️⃣:"
        )
        return ASK_OPTION_1

    context.user_data["current_question"]["option1"] = option1_text
    await update.message.reply_text(
        "Вариант 1 принят. Введите текст для второго варианта ответа (2️⃣):"
    )
    return ASK_OPTION_2


async def ask_option_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет вариант 2 и запрашивает вариант 3."""
    option2_text = update.message.text
    if not option2_text:
        await update.message.reply_text(
            "Вариант ответа не может быть пустым. Введите текст для варианта 2️⃣:"
        )
        return ASK_OPTION_2

    context.user_data["current_question"]["option2"] = option2_text
    await update.message.reply_text(
        "Вариант 2 принят. Введите текст для третьего варианта ответа (3️⃣):"
    )
    return ASK_OPTION_3


async def ask_option_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет вариант 3 и запрашивает вариант 4."""
    option3_text = update.message.text
    if not option3_text:
        await update.message.reply_text(
            "Вариант ответа не может быть пустым. Введите текст для варианта 3️⃣:"
        )
        return ASK_OPTION_3

    context.user_data["current_question"]["option3"] = option3_text
    await update.message.reply_text(
        "Вариант 3 принят. Введите текст для четвертого варианта ответа (4️⃣):"
    )
    return ASK_OPTION_4


async def ask_option_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет вариант 4 и запрашивает номер правильного ответа."""
    option4_text = update.message.text
    if not option4_text:
        await update.message.reply_text(
            "Вариант ответа не может быть пустым. Введите текст для варианта 4️⃣:"
        )
        return ASK_OPTION_4

    context.user_data["current_question"]["option4"] = option4_text
    await update.message.reply_text(
        "Вариант 4 принят. Теперь введите номер правильного варианта ответа (от 1 до 4):"
    )
    return ASK_CORRECT_OPTION


async def ask_correct_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет номер правильного ответа и спрашивает, добавить ли еще вопрос."""
    try:
        correct_option = int(update.message.text)
        if not 1 <= correct_option <= 4:
            raise ValueError("Номер должен быть от 1 до 4.")
    except (ValueError, TypeError):
        await update.message.reply_text(
            "Неверный ввод. Пожалуйста, введите число от 1 до 4, соответствующее правильному варианту:"
        )
        return ASK_CORRECT_OPTION

    # Сохраняем готовый вопрос в список вопросов теста
    current_q = context.user_data["current_question"]
    current_q["correct_option"] = correct_option
    context.user_data["new_test"]["questions"].append(current_q.copy())

    # Очищаем данные для следующего вопроса
    context.user_data["current_question"] = {}

    keyboard = [
        [
            InlineKeyboardButton(
                "➕ Добавить еще вопрос", callback_data="add_another_q"
            ),
            InlineKeyboardButton(
                "✅ Завершить создание", callback_data="finish_creation"
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Вопрос '{current_q['text'][:30]}...' добавлен. Хотите добавить еще один вопрос или завершить создание теста?",
        reply_markup=reply_markup,
    )
    return CONFIRM_ADD_QUESTION


async def confirm_add_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Обрабатывает ответ пользователя: добавить еще вопрос или завершить."""
    query = update.callback_query
    await query.answer()
    command = query.data

    if command == "add_another_q":
        await query.edit_message_text("Хорошо, введите текст следующего вопроса:")
        return ASK_QUESTION
    elif command == "finish_creation":
        # Переходим к завершению
        return await finish_test_creation(update, context)
    else:
        # На всякий случай, если будет другой callback_data
        await query.edit_message_text("Неизвестная команда.")
        return CONFIRM_ADD_QUESTION


async def finish_test_creation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Завершает создание теста, сохраняет его и возвращает пользователя."""
    user_id = update.callback_query.from_user.id
    username = (
        update.callback_query.from_user.username or f"User_{user_id}"
    )  # Сохраняем username
    new_test_data = context.user_data.get("new_test")

    if not new_test_data or not new_test_data.get("questions"):
        await update.callback_query.edit_message_text(
            "Не удалось завершить создание: нет данных о тесте или вопросов. Попробуйте создать заново.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
            ),  # Кнопка на главное меню
        )
        # Очищаем временные данные
        if "new_test" in context.user_data:
            del context.user_data["new_test"]
        if "current_question" in context.user_data:
            del context.user_data["current_question"]
        return ConversationHandler.END

    # Добавляем автора
    new_test_data["author_id"] = user_id
    new_test_data["author_username"] = username

    # Добавляем тест в хранилище
    if user_id not in custom_tests_storage:
        custom_tests_storage[user_id] = []
    custom_tests_storage[user_id].append(new_test_data)

    # Сохраняем все тесты в файл
    save_custom_tests(custom_tests_storage)

    await update.callback_query.edit_message_text(
        f"🎉 Тест '{new_test_data['name']}' успешно создан и сохранен! В нем {len(new_test_data['questions'])} вопросов.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
        ),  # Кнопка на главное меню
    )

    # Очищаем временные данные
    del context.user_data["new_test"]
    if "current_question" in context.user_data:
        del context.user_data["current_question"]

    return ConversationHandler.END


async def cancel_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет процесс создания теста и возвращает в главное меню."""
    # Импортируем здесь, чтобы избежать циклического импорта
    from bot import main_menu

    query = update.callback_query
    message = update.message  # Может быть вызвано командой /cancel

    # Определяем, откуда пришла отмена
    if query:
        await query.answer()
        await query.edit_message_text(
            "Создание теста отменено.", reply_markup=None  # Убираем клавиатуру диалога
        )
        # Отправляем новое сообщение с главным меню
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text="Возвращаемся в главное меню.",
        )
        # Создаем фейковый update с сообщением для main_menu
        fake_update = Update(
            update_id=0, message=query.message
        )  # Используем исходное сообщение callback-а
        await main_menu(fake_update, context)  # Вызываем главное меню

    elif message:
        await message.reply_text(
            "Создание теста отменено.", reply_markup=ReplyKeyboardRemove()
        )
        await main_menu(update, context)  # Вызываем главное меню

    # Очищаем временные данные
    if "new_test" in context.user_data:
        del context.user_data["new_test"]
    if "current_question" in context.user_data:
        del context.user_data["current_question"]

    return ConversationHandler.END


# --- Обработчик для показа каталога ---


async def show_test_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает каталог кастомных тестов с пагинацией."""
    query = update.callback_query
    await query.answer()

    # Определяем текущую страницу
    current_page = 0
    if query.data and query.data.startswith("test_catalog_"):
        try:
            current_page = int(query.data.split("_")[-1])
        except (ValueError, IndexError):
            current_page = 0

    # Собираем все тесты в один список
    all_tests_flat = []
    for author_id, tests in custom_tests_storage.items():
        for index, test in enumerate(tests):
            test_info = test.copy()  # Копируем, чтобы добавить author_id и index
            test_info["author_id"] = author_id
            test_info["test_index"] = index
            all_tests_flat.append(test_info)

    if not all_tests_flat:
        await query.edit_message_text(
            "Кастомных тестов пока нет. 😢\nНажмите '📝 Создать свой тест', чтобы добавить первый!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
            ),
        )
        return

    # Пагинация
    total_tests = len(all_tests_flat)
    start_index = current_page * TESTS_PER_PAGE
    end_index = start_index + TESTS_PER_PAGE
    tests_on_page = all_tests_flat[start_index:end_index]
    total_pages = (total_tests + TESTS_PER_PAGE - 1) // TESTS_PER_PAGE

    # Формируем текст и кнопки для текущей страницы
    test_list_text = ""
    keyboard = []
    for test in tests_on_page:
        author_id = test["author_id"]
        index = test["test_index"]
        author_name = test.get("author_username", f"User_{author_id}")
        test_name = test.get("name", "Без названия")
        num_questions = len(test.get("questions", []))
        callback_data = f"run_custom_{author_id}_{index}"

        test_list_text += f"\n🔹 '{test_name}' от {author_name} ({num_questions} вопр.)"
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"▶️ Запустить '{test_name}'", callback_data=callback_data
                )
            ]
        )

    # Добавляем кнопки пагинации
    pagination_buttons = []
    if current_page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                "◀️ Назад", callback_data=f"test_catalog_{current_page - 1}"
            )
        )
    if end_index < total_tests:
        pagination_buttons.append(
            InlineKeyboardButton(
                "Вперед ▶️", callback_data=f"test_catalog_{current_page + 1}"
            )
        )

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    # Добавляем кнопку "Главное меню"
    keyboard.append(
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    )

    # Формируем итоговый текст
    text = f"📚 Каталог кастомных тестов (Страница {current_page + 1}/{total_pages}):{test_list_text}"
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text, reply_markup=reply_markup)


# --- Обработчик для запуска кастомного теста ---


async def run_custom_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Инициализирует и запускает кастомный тест."""
    query = update.callback_query
    await query.answer()
    callback_data = query.data
    user_id = query.from_user.id

    try:
        _, _, author_id_str, test_index_str = callback_data.split("_")
        author_id = int(author_id_str)
        test_index = int(test_index_str)

        # Находим тест в хранилище
        test_data = custom_tests_storage.get(author_id, [])[test_index]
        test_name = test_data.get("name", "Без названия")
        questions = test_data.get("questions", [])

        if not questions:
            await query.edit_message_text(
                f"❌ Тест '{test_name}' пуст (нет вопросов).",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "⬅️ Назад в каталог", callback_data="test_catalog"
                            )
                        ]
                    ]
                ),
            )
            return

        # Инициализируем состояние теста в user_data
        context.user_data["custom_test"] = {
            "name": test_name,
            "questions": questions,
            "current_question_index": 0,
            "correct_answers": 0,
            "total_questions": len(questions),
        }

        await query.edit_message_text(
            f"📚 Начинаем кастомный тест '{test_name}'!\n"
            f"Всего вопросов: {len(questions)}. Удачи! 🍀"
        )

        # Отправляем первый вопрос
        await send_custom_question(update, context, user_id)

    except (ValueError, IndexError, KeyError) as e:
        logging.error(f"Ошибка при запуске кастомного теста ({callback_data}): {e}")
        await query.edit_message_text(
            "❌ Не удалось найти или запустить выбранный тест. Возможно, он был удален.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⬅️ Назад в каталог", callback_data="test_catalog"
                        )
                    ]
                ]
            ),
        )


async def send_custom_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int
):
    """Отправляет текущий вопрос кастомного теста."""
    test_state = context.user_data.get("custom_test")
    if not test_state:
        logging.warning(
            f"Попытка отправить кастомный вопрос без состояния теста для user_id={user_id}"
        )
        # Возможно, стоит вернуть пользователя в каталог или меню
        return

    current_index = test_state["current_question_index"]
    total_questions = test_state["total_questions"]

    if current_index >= total_questions:
        # Тест завершен
        await finish_custom_test(update, context, user_id)
        return

    question_data = test_state["questions"][current_index]

    # Формируем текст вопроса
    question_text = (
        f"❓ Вопрос {current_index + 1}/{total_questions}:\n\n"
        f"{question_data['text']}\n\n"
        f"Варианты ответов:\n"
        f"1️⃣ {question_data['option1']}\n"
        f"2️⃣ {question_data['option2']}\n"
        f"3️⃣ {question_data['option3']}\n"
        f"4️⃣ {question_data['option4']}"
    )

    # Формируем кнопки ответов
    keyboard = [
        [
            InlineKeyboardButton("1️⃣", callback_data="custom_answer_1"),
            InlineKeyboardButton("2️⃣", callback_data="custom_answer_2"),
            InlineKeyboardButton("3️⃣", callback_data="custom_answer_3"),
            InlineKeyboardButton("4️⃣", callback_data="custom_answer_4"),
        ],
        # TODO: Добавить кнопку отмены/выхода из теста?
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем вопрос новым сообщением
    await context.bot.send_message(
        chat_id=user_id, text=question_text, reply_markup=reply_markup
    )


async def handle_custom_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает ответ пользователя на вопрос кастомного теста."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    selected_option = int(query.data.split("_")[2])  # custom_answer_X

    test_state = context.user_data.get("custom_test")
    if not test_state:
        logging.warning(
            f"Получен ответ на кастомный тест без состояния теста для user_id={user_id}"
        )
        await query.edit_message_text(
            "Произошла ошибка, состояние теста потеряно. Попробуйте начать заново."
        )
        # TODO: Вернуть в меню/каталог
        return

    current_index = test_state["current_question_index"]
    if current_index >= test_state["total_questions"]:
        logging.warning(f"Получен лишний ответ на кастомный тест для user_id={user_id}")
        await query.edit_message_text("Тест уже завершен.")
        return  # Тест уже завершен

    question_data = test_state["questions"][current_index]
    correct_option = question_data["correct_option"]
    is_correct = selected_option == correct_option

    # Формируем текст вопроса для обратной связи
    total_questions = test_state["total_questions"]
    question_text_feedback = (
        f"❓ Вопрос {current_index + 1}/{total_questions}:\n\n"
        f"{question_data['text']}\n\n"
        f"Варианты ответов:\n"
        f"1️⃣ {question_data['option1']}\n"
        f"2️⃣ {question_data['option2']}\n"
        f"3️⃣ {question_data['option3']}\n"
        f"4️⃣ {question_data['option4']}"
    )

    # Формируем обратную связь
    selected_answer_text = question_data.get(
        f"option{selected_option}", "Неизвестный вариант"
    )
    if is_correct:
        test_state["correct_answers"] += 1
        feedback = (
            f"{question_text_feedback}\n\n"
            "✅ Правильно!\n\n"
            f"Ваш ответ: {selected_answer_text}"
        )
    else:
        correct_answer_text = question_data.get(
            f"option{correct_option}", "Неизвестный вариант"
        )
        feedback = (
            f"{question_text_feedback}\n\n"
            "❌ Неправильно!\n\n"
            f"Ваш ответ: {selected_answer_text}\n"
            f"Правильный ответ: {correct_answer_text}"
        )

    # Обновляем сообщение с вопросом, убирая кнопки и показывая результат
    await query.edit_message_text(text=feedback, reply_markup=None)

    # Переходим к следующему вопросу
    test_state["current_question_index"] += 1
    await send_custom_question(update, context, user_id)


async def finish_custom_test(
    update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int
):
    """Завершает кастомный тест, показывает результаты и обновляет MMR."""
    test_state = context.user_data.get("custom_test")
    if not test_state:
        logging.warning(
            f"Попытка завершить кастомный тест без состояния для user_id={user_id}"
        )
        return

    correct_answers = test_state["correct_answers"]
    total_questions = test_state["total_questions"]
    test_name = test_state["name"]
    username = update.effective_user.username or f"User_{user_id}"

    percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    # --- Расчет и обновление MMR ---
    mmr_change = 0
    new_mmr = 0
    old_mmr = 0
    stats_text = ""
    try:
        with get_db() as db:
            stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
            if not stats:
                # Создаем статистику, если ее нет
                stats = UserStats(user_id=user_id, username=username)
                db.add(stats)
                db.flush()  # Получаем ID и начальный MMR

            if stats:
                old_mmr = stats.mmr
                mmr_change = stats.calculate_mmr_change_custom(
                    correct_answers, total_questions
                )
                stats.mmr = max(
                    0, stats.mmr + mmr_change
                )  # MMR не может быть отрицательным
                stats.total_tests += 1
                stats.last_test_date = datetime.utcnow()
                stats.username = username  # Обновляем имя пользователя на всякий случай
                new_mmr = stats.mmr
                db.commit()

                # Формируем текст об изменении MMR
                mmr_symbol = (
                    "🔺" if mmr_change > 0 else "🔻" if mmr_change < 0 else "➖"
                )
                stats_text = f"\n\n📊 Статистика:\nMMR: {old_mmr} {mmr_symbol} {abs(mmr_change)} = {new_mmr}"
            else:
                logging.error(
                    f"Не удалось найти или создать статистику для user_id={user_id}"
                )

    except Exception as e:
        logging.error(f"Ошибка при обновлении MMR для user_id={user_id}: {e}")
        stats_text = "\n\n⚠️ Не удалось обновить MMR из-за ошибки."
    # --- Конец расчета MMR ---

    # Оценка результата
    if percentage == 100:
        grade = "🏆 Отлично! Все ответы верны!"
    elif percentage >= 75:
        grade = "👍 Хороший результат!"
    elif percentage >= 50:
        grade = "🙂 Неплохо, но можно лучше."
    else:
        grade = "💪 Старайтесь усерднее!"

    result_text = (
        f"🏁 Тест '{test_name}' завершен!\n\n"
        f"{grade}\n\n"
        f"Правильных ответов: {correct_answers}/{total_questions} ({percentage:.1f}%) {stats_text}"  # Добавляем текст MMR
    )

    # Сначала отправляем сообщение с результатами
    # Используем исходный query для отправки ответа, если он есть
    final_message_target = (
        update.callback_query.message if update.callback_query else None
    )
    try:
        if final_message_target:
            # Пытаемся отредактировать последнее сообщение (с результатом предыдущего ответа)
            await final_message_target.edit_text(text=result_text, reply_markup=None)
        else:
            # Если не можем редактировать (например, при ошибке), отправляем новое
            await context.bot.send_message(chat_id=user_id, text=result_text)

        # Затем отправляем новое сообщение с кнопками навигации
        keyboard = [
            [InlineKeyboardButton("📚 Назад в каталог", callback_data="test_catalog")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=user_id,
            text="Выберите дальнейшее действие:",
            reply_markup=reply_markup,
        )

    except Exception as e:
        logging.error(f"Ошибка при отображении результатов кастомного теста: {e}")
        # Если не удалось отправить результаты, все равно очищаем состояние

    # Очищаем состояние теста из user_data
    if "custom_test" in context.user_data:
        del context.user_data["custom_test"]
