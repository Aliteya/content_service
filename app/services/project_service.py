from ..repositories import ProjectRepository
from .file_service import FileService
from ..schemas import ProjectReadDTO, ProjectCreateEditDTO, FileCreateSchema, ProjectHistoryReadDTO, Category
from sqlalchemy.ext.asyncio import AsyncSession

class ProjectService:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
        self.project_repo = ProjectRepository(self.session)
        self.file_service = FileService(self.session)
        
    async def get_project_by_id(self, project_id: int) -> ProjectReadDTO:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Проект с id={project_id} не найден.")

        hist_map = []
        for history in project.histories:
            hist_map.append(
                ProjectHistoryReadDTO(
                    project_id=project_id,
                    type=history.type,
                    fileName=history.file.name,
                    filter=history.filter,
                    startTime=history.startTime,
                    endTime=history.endTime,
                )
            )
        
        return ProjectReadDTO(
            id=project.id,
            projectName=project.projectName,
            category=project.category,
            my_histories=hist_map,
        )

    async def delete_project_by_id(self, project_id: int) -> str:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Проект с id={project_id} не найден.")
        
        await self.file_service.delete_file_project(project_id)

        result = await self.project_repo.delete_by_id(project_id)
        if not result:
            raise RuntimeError(f"Ошибка при удалении проекта id={project_id}.")

        return f"Проект id={project_id} успешно удален."

    async def update_project_by_id(self, project_id: int, project_create_edit_dto: ProjectCreateEditDTO) -> bool:
        project = await self.project_repo.update_by_id(project_id, project_create_edit_dto.model_dump())
        if not project:
            raise ValueError(f"Ошибка при обновлении проекта id={project_id}.")
        return project

    async def create_new_project(self, name: str, category: Category):
        new_project_data = {"projectName": name, "category": category}
        project = await self.project_repo.save_project(new_project_data)        
        if not project:
            raise RuntimeError("Не удалось создать проект.")
        return project

