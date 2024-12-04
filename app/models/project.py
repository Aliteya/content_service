from .base import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

class Category(Enum):
    EDUCATIONAL = "EDUCATIONAL"
    CLIP = 'CLIP'
    STORYTELLING = "STORYTELLING"
    FUNNY = "FUNNY"
    VLOG = "VLOG"
    TRAILER = "TRAILER"

class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    projectName: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[Category] = mapped_column(SQLAlchemyEnum(Category),nullable=False)

    histories = relationship("History", back_populates="project")
