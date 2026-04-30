from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import date

class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    assignee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    due_date: Optional[date]
    project_id: int
    assignee_id: Optional[int]
    created_by: int

    class Config:
        from_attributes = True