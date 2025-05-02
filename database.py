from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from contextlib import contextmanager

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    level = Column(String, nullable=False)  # junior, middle, senior
    question_text = Column(String, nullable=False)
    option1 = Column(String, nullable=False)
    option2 = Column(String, nullable=False)
    option3 = Column(String, nullable=False)
    option4 = Column(String, nullable=False)
    correct_option = Column(Integer, nullable=False)  # 1-4


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    level = Column(String, nullable=False)
    current_question = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    is_testing = Column(Boolean, default=False)
    last_answer_time = Column(DateTime, default=datetime.utcnow)
    question_ids = Column(
        String, nullable=True
    )  # Хранит ID выбранных вопросов через запятую


class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    mmr = Column(Integer, default=1000)  # Начальный MMR
    total_tests = Column(Integer, default=0)
    last_test_date = Column(DateTime)

    def calculate_mmr_change(
        self, correct_answers: int, difficulty_level: str, opponent_mmr: int = 1500
    ):
        # Базовые очки за каждый правильный ответ
        base_points = 25

        # Множитель сложности
        difficulty_multiplier = {
            "junior": 1.0,
            "middle": 1.5,
            "senior": 2.0,
            "junior_python": 1.0,
            "middle_python": 1.5,
            "senior_python": 2.0,
            "junior_sql": 1.0,
            "middle_sql": 1.5,
            "senior_sql": 2.0,
            "junior_java": 1.0,
            "middle_java": 1.5,
            "senior_java": 2.0,
        }

        # Получаем множитель сложности
        level_multiplier = difficulty_multiplier.get(difficulty_level.lower(), 1.0)

        # Рассчитываем процент правильных ответов
        score_percentage = (correct_answers / 10) * 100

        # Новая система штрафов и наград
        if score_percentage < 30:  # Очень плохой результат
            mmr_change = int(-80 * level_multiplier)  # Большой штраф
        elif score_percentage < 50:  # Плохой результат
            mmr_change = int(-50 * level_multiplier)  # Средний штраф
        elif score_percentage < 70:  # Средний результат
            mmr_change = int(-20 * level_multiplier)  # Небольшой штраф
        elif score_percentage < 90:  # Хороший результат
            mmr_change = int(30 * level_multiplier)  # Небольшая награда
        else:  # Отличный результат
            mmr_change = int(50 * level_multiplier)  # Большая награда

        # Дополнительный множитель для защиты новичков
        if self.mmr < 800:  # Защита новичков от больших потерь
            if mmr_change < 0:
                mmr_change = int(mmr_change * 0.5)  # Уменьшаем штраф вдвое
        elif self.mmr > 2000:  # Более строгие правила для опытных
            if mmr_change < 0:
                mmr_change = int(mmr_change * 1.5)  # Увеличиваем штраф в 1.5 раза

        # Защита от слишком больших изменений
        mmr_change = max(min(mmr_change, 150), -100)

        return mmr_change

    def calculate_mmr_change_custom(self, correct_answers: int, total_questions: int):
        """Рассчитывает изменение MMR для кастомного теста."""
        if total_questions == 0:
            return 0  # Нет вопросов - нет изменения MMR

        score_percentage = (correct_answers / total_questions) * 100

        # Базовые изменения MMR для кастомных тестов (без учета уровня)
        if score_percentage < 30:
            mmr_change = -50
        elif score_percentage < 50:
            mmr_change = -30
        elif score_percentage < 70:
            mmr_change = -15
        elif score_percentage < 90:
            mmr_change = 20
        else:
            mmr_change = 40

        # Применяем общие правила (защита новичков, штрафы для опытных)
        if self.mmr < 800:
            if mmr_change < 0:
                mmr_change = int(mmr_change * 0.5)
        elif self.mmr > 2000:
            if mmr_change < 0:
                mmr_change = int(mmr_change * 1.5)

        # Ограничение на максимальное/минимальное изменение (можно настроить)
        mmr_change = max(
            min(mmr_change, 100), -75
        )  # Немного другие рамки для кастомных

        return mmr_change


# Создаем подключение к базе данных
engine = create_engine("sqlite:///asu_quiz.db")
SessionLocal = sessionmaker(bind=engine)


# Создаем таблицы
def create_tables():
    Base.metadata.create_all(engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
