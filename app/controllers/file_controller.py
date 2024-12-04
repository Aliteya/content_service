from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import FileService
from ..schemas import FileSchema
from ..database import get_session

file_router = APIRouter(prefix="/files", tags=["files"])

def get_file_service(session: AsyncSession = Depends(get_session)) -> FileService:
    return FileService(session)

@file_router.post("/")
async def add_file(file: FileSchema, file_service: FileService = Depends(get_file_service)):
    result = await file_service.add_file(file)
    if result:
        return {"message": "Файл успешно добавлен"}
    raise HTTPException(status_code=400, detail="Не удалось добавить файл")


@file_router.get("/{filename}")
async def get_file(filename: str, file_service: FileService = Depends(get_file_service)):
    file = await file_service.get_file(filename)
    if file:
        return file
    raise HTTPException(status_code=404, detail="Файл не найден")


@file_router.get("/project/{project_id}")
async def get_files_by_project(project_id: int, file_service: FileService = Depends(get_file_service)):
    files = await file_service.get_files_by_project(project_id)
    if files:
        return files
    return {"message": "Файлы для указанного проекта не найдены"}


@file_router.delete("/{filename}")
async def delete_file(filename: str, file_service: FileService = Depends(get_file_service)):
    result = await file_service.delete_file_filename(filename)
    if result:
        return {"message": "Файл успешно удален"}
    raise HTTPException(status_code=400, detail="Не удалось удалить файл")
