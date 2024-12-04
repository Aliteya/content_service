from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import ProjectHistoryReadDTO, ProjectHistoryCreateEditDTO
from ..services import ProjectHistoryService
from ..database import get_session

history_router = APIRouter(prefix="/project-history", tags=["project history"])


def get_project_history_service(session: AsyncSession = Depends(get_session)) -> ProjectHistoryService:
    return ProjectHistoryService(session)


@history_router.get("/{project_id}")
async def get_project_history(project_id: int, service: ProjectHistoryService = Depends(get_project_history_service)):
    histories = await service.get_project_history(project_id)
    if not histories:
        raise HTTPException(status_code=404, detail="История проекта не найдена")
    return histories


@history_router.post("/{project_id}")
async def add_project_history(
    project_id: int,
    history_data: ProjectHistoryCreateEditDTO,
    service: ProjectHistoryService = Depends(get_project_history_service)
):
    success = await service.add_project_history(project_id, history_data)
    if success:
        return {"message": "Запись успешно добавлена в историю проекта"}
    raise HTTPException(status_code=400, detail="Не удалось добавить запись в историю проекта")
