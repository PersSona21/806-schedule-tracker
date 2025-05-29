from pydantic import BaseModel, Field
from typing import Optional

class LessonBase(BaseModel):
    day: str
    subject: str
    lesson_type: str
    start_time: str
    end_time: str
    teachers: str
    location: str
    is_custom: Optional[bool] = Field(False)
    recurrence: Optional[str] = Field(None, nullable=True)
    is_synced: Optional[bool] = Field(False)

class LessonCreate(LessonBase):
    pass

class Lesson(LessonBase):
    id: int

    class Config:
        orm_mode = True