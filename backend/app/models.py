"""
SQLAlchemy database models.
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from .database import Base
import enum


class CategoryEnum(str, enum.Enum):
    """Task category enumeration."""
    work = "work"
    personal = "personal"
    shopping = "shopping"
    other = "other"


class PriorityEnum(str, enum.Enum):
    """Task priority enumeration."""
    low = "low"
    medium = "medium"
    high = "high"


class StatusEnum(str, enum.Enum):
    """Task status enumeration."""
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Task(Base):
    """
    Task model representing a task in the task manager.

    Attributes:
        id: Unique identifier for the task
        title: Task title (required)
        description: Detailed description of the task (optional)
        category: Task category (work, personal, shopping, other)
        priority: Task priority (low, medium, high)
        status: Current status (pending, in_progress, completed)
        due_date: Optional due date for the task
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(Enum(CategoryEnum), default=CategoryEnum.other, nullable=False)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.medium, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending, nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
