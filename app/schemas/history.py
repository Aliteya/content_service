from pydantic import BaseModel
from typing import List
from datetime import date
from enum import Enum

class FilterType(str, Enum):
    NONE = "NONE"
    SPEED = "SPEED"
    CROPPING = "CROPPING"
    GLUING = "GLUING"

class HistoryType(str, Enum):
    EDIT = "EDIT"
    DELETE = "DELETE" 
    ADD =  "ADD"
    APPLY = "APPLY"

class ProjectHistoryReadDTO(BaseModel):
    project_id: int
    type: HistoryType
    fileName: str
    filter: FilterType
    startTime: str
    endTime: str

class ProjectHistoryCreateEditDTO(BaseModel):
    type: HistoryType
    file_id: int
    author_id: int
    filter: FilterType
    startTime: date
    endTime: date