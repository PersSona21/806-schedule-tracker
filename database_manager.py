from postgresql.crud import add_lesson, get_lessons
from postgresql.create_table import create_table
from postgresql import schemas
from postgresql.database import SessionLocal

class Database_manager:
    def __init__(self):
        self.db = SessionLocal()
        create_table()


    def add_lesson(self, lesson: dict):
        lesson['teachers'] = ', '.join(lesson['teachers']) # Превращиение списка в строку
        processed_lesson = schemas.LessonCreate(**lesson)
        add_lesson(db=self.db, lesson=processed_lesson)
    

    def get_lessons(self, skip: int = 0, limit: int = 100):
        return get_lessons(self.db, skip, limit)
    
    def close(self):
        self.db.close()