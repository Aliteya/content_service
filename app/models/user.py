from .base import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

class SubscriptionType(Enum):
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    UNLIMITED = "UNLIMITED"

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    fullName: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    personalPhoto: Mapped[bytes] = mapped_column(nullable=True)
    telephoneNumber: Mapped[str] = mapped_column(nullable=True)

    subscription: Mapped[SubscriptionType] = mapped_column(SQLAlchemyEnum(SubscriptionType), nullable=True)

    histories = relationship("History", back_populates="author")