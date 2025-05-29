from sqlalchemy.orm import Session
from . import models, schemas

def add_lesson(db: Session, lesson: schemas.LessonCreate):
    db_lesson = models.Schedule(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def get_lessons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Schedule).offset(skip).limit(limit).all()