from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from app.database import Base
import enum

class TaskStatus(enum.Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    due_date = Column(Date, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    