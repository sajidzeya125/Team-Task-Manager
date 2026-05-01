from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.task import Task
from app.models.project_member import ProjectMember
from app.models.user import User, UserRole
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/projects/{project_id}", response_model=TaskOut)
def create_task(
    project_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    if not is_member and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a project member")

    task = Task(
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        assignee_id=payload.assignee_id,
        project_id=project_id,
        created_by=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/projects/{project_id}", response_model=list[TaskOut])
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    if not is_member and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a project member")

    return db.query(Task).filter(Task.project_id == project_id).all()

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if current_user.role != UserRole.admin and task.assignee_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    if payload.status:
        task.status = payload.status
    if payload.assignee_id:
        task.assignee_id = payload.assignee_id

    db.commit()
    db.refresh(task)
    return task