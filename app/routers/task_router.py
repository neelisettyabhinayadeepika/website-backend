from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.user import User

from app.schemas.task_schema import TaskCreate

from app.services.task_service import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def add_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(db, task, user_id=current_user.id)


@router.get("/")
def get_tasks(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_all_tasks(db)


@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}")
def edit_task(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_obj = update_task(db, task_id, task)

    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_obj


@router.delete("/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_obj = delete_task(db, task_id)

    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_obj
