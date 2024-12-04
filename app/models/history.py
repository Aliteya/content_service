from .base import Base

from .project import Project
from .user import User
from .file import File

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import date
from sqlalchemy import Enum as SQLAlchemyEnum

class FilterType(Enum):
    NONE = "NONE"
    SPEED = "SPEED"
    CROPPING = "CROPPING"
    GLUING = "GLUING"

class HistoryType(Enum):
    EDIT = "EDIT"
    DELETE = "DELETE" 
    ADD =  "ADD"
    APPLY = "APPLY"

class History(Base):
    __tablename__ = 'histories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    type: Mapped[HistoryType] = mapped_column(SQLAlchemyEnum(HistoryType))
    filter: Mapped[FilterType] = mapped_column(SQLAlchemyEnum(FilterType))
    
    startTime: Mapped[date] = mapped_column(nullable=False)
    endTime: Mapped[date] = mapped_column(nullable=False)

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)
    file_id: Mapped[int] = mapped_column(ForeignKey('files.id'), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    project = relationship("Project", back_populates='histories')
    author = relationship("User", back_populates='histories')
    file = relationship("File")

    