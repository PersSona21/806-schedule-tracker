from sqlalchemy import Column, Integer, String, Boolean
from postgresql.database import Base
class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    day = Column(String)
    subject = Column(String)
    lesson_type = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    teachers = Column(String)
    location = Column(String)    
    is_custom = Column(Boolean, default=False)
    recurrence = Column(String, nullable=True)
    is_synced = Column(Boolean, default=False)