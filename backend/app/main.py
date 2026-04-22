"""
FastAPI application entry point.
Task Manager API with CRUD operations.
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from . import crud, models, schemas
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Task Manager API",
    description="A simple task management REST API built with FastAPI and PostgreSQL",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "task-manager-api"}


@app.get("/api/tasks", response_model=List[schemas.Task])
def read_tasks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all tasks with optional filtering and pagination.

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **category**: Filter by category (work, personal, shopping, other)
    - **status**: Filter by status (pending, in_progress, completed)
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit, category=category, status=status)
    return tasks


@app.get("/api/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by ID.

    - **task_id**: ID of the task to retrieve
    """
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/tasks", response_model=schemas.Task, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.

    - **title**: Task title (required, 1-200 characters)
    - **description**: Task description (optional, max 1000 characters)
    - **category**: Task category (work, personal, shopping, other)
    - **priority**: Task priority (low, medium, high)
    - **status**: Task status (pending, in_progress, completed)
    - **due_date**: Optional due date (ISO 8601 format)
    """
    return crud.create_task(db=db, task=task)


@app.put("/api/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    All fields are optional - only provided fields will be updated.

    - **task_id**: ID of the task to update
    """
    updated_task = crud.update_task(db=db, task_id=task_id, task=task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@app.delete("/api/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task.

    - **task_id**: ID of the task to delete
    """
    deleted_task = crud.delete_task(db=db, task_id=task_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task


@app.get("/api/tasks/category/{category}", response_model=List[schemas.Task])
def read_tasks_by_category(category: str, db: Session = Depends(get_db)):
    """
    Retrieve all tasks in a specific category.

    - **category**: Category to filter by (work, personal, shopping, other)
    """
    # Validate category
    valid_categories = ["work", "personal", "shopping", "other"]
    if category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        )

    return crud.get_tasks_by_category(db=db, category=category)


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Get statistics about tasks.
    Returns total count and counts by status.
    """
    total = crud.get_tasks_count(db)

    pending = len(crud.get_tasks(db, status="pending", limit=10000))
    in_progress = len(crud.get_tasks(db, status="in_progress", limit=10000))
    completed = len(crud.get_tasks(db, status="completed", limit=10000))

    return {
        "total_tasks": total,
        "by_status": {
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
