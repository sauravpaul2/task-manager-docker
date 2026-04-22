"""
CRUD (Create, Read, Update, Delete) operations for tasks.
"""
from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    status: Optional[str] = None
) -> list[models.Task]:
    """
    Retrieve tasks with optional filtering.

    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        category: Optional category filter
        status: Optional status filter

    Returns:
        List of Task objects
    """
    query = db.query(models.Task)

    if category:
        query = query.filter(models.Task.category == category)

    if status:
        query = query.filter(models.Task.status == status)

    return query.offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    """
    Retrieve a single task by ID.

    Args:
        db: Database session
        task_id: ID of the task to retrieve

    Returns:
        Task object if found, None otherwise
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """
    Create a new task.

    Args:
        db: Database session
        task: Task data from request

    Returns:
        Created Task object
    """
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session,
    task_id: int,
    task: schemas.TaskUpdate
) -> Optional[models.Task]:
    """
    Update an existing task.

    Args:
        db: Database session
        task_id: ID of the task to update
        task: Updated task data

    Returns:
        Updated Task object if found, None otherwise
    """
    db_task = get_task(db, task_id)

    if db_task is None:
        return None

    # Update only provided fields
    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> Optional[models.Task]:
    """
    Delete a task.

    Args:
        db: Database session
        task_id: ID of the task to delete

    Returns:
        Deleted Task object if found, None otherwise
    """
    db_task = get_task(db, task_id)

    if db_task is None:
        return None

    db.delete(db_task)
    db.commit()
    return db_task


def get_tasks_count(db: Session) -> int:
    """
    Get total count of tasks.

    Args:
        db: Database session

    Returns:
        Total number of tasks
    """
    return db.query(models.Task).count()


def get_tasks_by_category(db: Session, category: str) -> list[models.Task]:
    """
    Retrieve all tasks in a specific category.

    Args:
        db: Database session
        category: Category to filter by

    Returns:
        List of Task objects in the specified category
    """
    return db.query(models.Task).filter(models.Task.category == category).all()
