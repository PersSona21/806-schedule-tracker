from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
import crud
import database_manager


router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.post("/", response_model=schemas.Lesson)
def create_lesson(lesson: schemas.LessonCreate, db: Session = Depends(database_manager.get_db)):
    return crud.create_lesson(db=db, lesson=lesson)

@router.get("/", response_model=list[schemas.Lesson])
def read_lessons(skip: int = 0, limit: int = 100, db: Session = Depends(database_manager.get_db)):
    lessons = crud.get_lessons(db, skip=skip, limit=limit)
    return lessons