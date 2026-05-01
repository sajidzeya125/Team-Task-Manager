from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.core.deps import get_db, get_current_user
from app.models.task import Task, TaskStatus
from app.models.user import User, UserRole

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Task)
    if current_user.role != UserRole.admin:
        query = query.filter(Task.assignee_id == current_user.id)

    total = query.count()
    todo = query.filter(Task.status == TaskStatus.TODO).count()
    in_progress = query.filter(Task.status == TaskStatus.IN_PROGRESS).count()
    done = query.filter(Task.status == TaskStatus.DONE).count()
    overdue = query.filter(Task.due_date != None, Task.due_date < date.today()).count()  # noqa

    return {
        "total": total,
        "todo": todo,
        "in_progress": in_progress,
        "done": done,
        "overdue": overdue,
    }