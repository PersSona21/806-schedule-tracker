from sqlalchemy import create_engine, Column, Integer, String, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    audience = Column(String)
    day = Column(String)
    start_time = Column(String)  # Или Time, если нужно
    end_time = Column(String)
    subject = Column(String)
    teacher = Column(String)
    is_custom = Column(Boolean, default=False)
    recurrence = Column(String, nullable=True)
    is_synced = Column(Boolean, default=False)  # Важная новая колонка!

# Подключение создаст новую БД с актуальной структурой
engine = create_engine("sqlite:///schedule.db")
Base.metadata.create_all(engine)  # Создаст таблицу заново
Session = sessionmaker(bind=engine)
