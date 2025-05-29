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
<<<<<<< HEAD
        from_attributes = True  # Заменяем orm_mode
=======
        orm_mode = True
>>>>>>> 78c0c4f8cc35a14f595b233cf407f299667c7fda
