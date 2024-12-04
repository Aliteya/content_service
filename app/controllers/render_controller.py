from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import RenderService
from ..schemas import ProjectCreateEditDTO, FileCreateSchema, ProjectHistoryCreateEditDTO
from ..database import get_session

render_router = APIRouter(prefix="/render", tags=["render"])


def get_render_service(session: AsyncSession = Depends(get_session)) -> RenderService:
    return RenderService(session)


@render_router.post("/")
async def create_project_with_file_and_history(
    project_data: ProjectCreateEditDTO,
    file_data: FileCreateSchema,
    history_data: ProjectHistoryCreateEditDTO,
    render_service: RenderService = Depends(get_render_service),
):
    try:
        project = await render_service.create_project_with_history_and_file(
            project_data, file_data, history_data
        )
        return {"message": "Проект успешно создан", "project": project}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при создании проекта: {e}")


@render_router.put("/{project_id}")
async def update_project_with_file_and_history(
    project_id: int,
    project_data: ProjectCreateEditDTO,
    file_data: FileCreateSchema,
    history_data: ProjectHistoryCreateEditDTO,
    render_service: RenderService = Depends(get_render_service),
):
    try:
        updated_project = await render_service.update_project_and_file_with_history(
            project_id, project_data, file_data, history_data
        )
        return {"message": "Проект успешно обновлен", "project": updated_project}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обновлении проекта: {e}")
