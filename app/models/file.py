from .base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

class FileType(Enum):
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"

class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[FileType] = mapped_column(SQLAlchemyEnum(FileType))
    name: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[bytes] = mapped_column()

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    project = relationship("Project")