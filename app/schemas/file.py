from pydantic import BaseModel

from enum import Enum

class FileType(str, Enum):
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"

class FileSchema(BaseModel):
    type: FileType 
    name: str
    body: bytes
    project_id: int

class FileCreateSchema(BaseModel):
    type: FileType 
    name: str
    body: bytes