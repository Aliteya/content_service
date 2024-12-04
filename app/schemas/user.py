from pydantic import BaseModel
from typing import List
from .project import ProjectReadDTO
from enum import Enum

class SubscriptionType(str, Enum):
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    UNLIMITED = "UNLIMITED"

class UserSchema(BaseModel):
    fullName: str 
    email: str
    telephoneNumber: str 
    subscription: SubscriptionType
    personalPhoto: bytes

class UserCreateEditDTO(BaseModel):
    fullName: str
    email: str
    password: str

class UserReadDTO(BaseModel):
    id: int
    fullName: str
    my_projects: List[ProjectReadDTO]