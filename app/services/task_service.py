from sqlalchemy.orm import Session
from app.models.task import Task


def create_task(db: Session, task, user_id: int):
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=user_id,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_all_tasks(db: Session):
    return db.query(Task).all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        return None

    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        return None

    db.delete(db_task)
    db.commit()

    return {"message": "Task deleted successfully"}
