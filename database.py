from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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
        }

        # Получаем множитель сложности
        level_multiplier = difficulty_multiplier.get(difficulty_level.lower(), 1.0)

        # Рассчитываем ожидаемый результат по формуле Эло
        expected_score = 1 / (1 + 10 ** ((opponent_mmr - self.mmr) / 400))

        # Фактический результат (процент правильных ответов)
        actual_score = correct_answers / 10

        # Рассчитываем изменение MMR
        mmr_change = int(
            base_points * level_multiplier * (actual_score - expected_score)
        )

        # Ограничиваем максимальное изменение MMR
        mmr_change = max(min(mmr_change, 100), -50)

        return mmr_change


# Создаем подключение к базе данных
engine = create_engine("sqlite:///java_quiz.db")
SessionLocal = sessionmaker(bind=engine)


# Создаем таблицы
def create_tables():
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
