from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import ProjectService
from ..schemas import ProjectReadDTO, ProjectCreateEditDTO, FileSchema, Category
from ..database import get_session

project_router = APIRouter(prefix="/projects", tags=["projects"])

def get_project_service(session: AsyncSession = Depends(get_session)) -> ProjectService:
    return ProjectService(session)

@project_router.post("/")
async def create_project(project_data: ProjectCreateEditDTO, project_service: ProjectService = Depends(get_project_service)):
    try:
        project = await project_service.create_new_project(project_data.projectName, project_data.category)
        return project
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@project_router.get("/{project_id}")
async def get_project(project_id: int, project_service: ProjectService = Depends(get_project_service)):
    try:
        project = await project_service.get_project_by_id(project_id)
        return project
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@project_router.put("/{project_id}")
async def update_project(project_id: int, project_data: ProjectCreateEditDTO, project_service: ProjectService = Depends(get_project_service)):
    try:
        updated_project = await project_service.update_project_by_id(project_id, project_data)
        return updated_project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@project_router.delete("/{project_id}")
async def delete_project(project_id: int, project_service: ProjectService = Depends(get_project_service)):
    try:
        message = await project_service.delete_project_by_id(project_id)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
