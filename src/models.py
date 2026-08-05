from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    workout_type = Column(String, index=True)
    duration_ms = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())