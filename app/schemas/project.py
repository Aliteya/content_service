from pydantic import BaseModel
from enum import Enum
from typing import List
from .history import ProjectHistoryReadDTO

class Category(str, Enum):
    EDUCATIONAL = "EDUCATIONAL"
    CLIP = "CLIP"
    STORYTELLING = "STORYTELLING"
    FUNNY = "FUNNY"
    VLOG = "VLOG"
    TRAILER = "TRAILER"

class ProjectSchema(BaseModel):
    projectName: Category
    category: str

class ProjectReadDTO(BaseModel):
    id: int
    projectName: str
    category: Category
    my_histories: List[ProjectHistoryReadDTO]

class ProjectCreateEditDTO(BaseModel):
    projectName: str
    category: Category
  
