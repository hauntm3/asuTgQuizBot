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
    user_id = Column(Integer, nullable=False)
    username = Column(String)
    total_tests = Column(Integer, default=0)
    junior_avg_score = Column(Float, default=0.0)
    middle_avg_score = Column(Float, default=0.0)
    senior_avg_score = Column(Float, default=0.0)
    best_score = Column(Float, default=0.0)
    last_test_date = Column(DateTime, default=datetime.utcnow)


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
