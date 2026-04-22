"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .models import CategoryEnum, PriorityEnum, StatusEnum


class TaskBase(BaseModel):
    """Base task schema with common attributes."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    category: CategoryEnum = Field(CategoryEnum.other, description="Task category")
    priority: PriorityEnum = Field(PriorityEnum.medium, description="Task priority")
    status: StatusEnum = Field(StatusEnum.pending, description="Task status")
    due_date: Optional[datetime] = Field(None, description="Task due date")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields are optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[CategoryEnum] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    due_date: Optional[datetime] = None


class Task(TaskBase):
    """
    Complete task schema with all fields including database-generated ones.
    Used for API responses.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy models


class TaskList(BaseModel):
    """Schema for paginated task list responses."""
    tasks: list[Task]
    total: int
    skip: int
    limit: int
