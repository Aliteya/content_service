from sqlalchemy.ext.asyncio import AsyncSession
from ..services import ProjectHistoryService, ProjectService, FileService
from ..repositories import MinioClient
from ..schemas import ProjectCreateEditDTO, ProjectCreateEditDTO, FileCreateSchema, ProjectHistoryCreateEditDTO
from sqlalchemy.ext.asyncio import AsyncSession

class RenderService:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
        self.pr_history_serv = ProjectHistoryService(self.session)
        self.project_serv = ProjectService(self.session)
        self.minio_client = MinioClient(self.session)
        self.file_serv = FileService(self.session)

    async def create_project_with_history_and_file(self, project_data: ProjectCreateEditDTO, file_data: FileCreateSchema, history_data: ProjectHistoryCreateEditDTO):
        try:
            new_project = await self.project_serv.create_new_project(project_data.projectName, project_data.category)
            
            project_id = new_project.id
            file_data.project_id = project_id
            print(file_data)
            file = await self.file_serv.add_file(file_data)
            file_id = file.id

            history_data.file_id = file_id
            await self.pr_history_serv.add_project_history(project_id, history_data)

            await self.session.commit()
            return new_project

        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error during project creation: {e}")

    async def update_project_and_file_with_history(self, project_id: int, project_data: ProjectCreateEditDTO, file_data: FileCreateSchema, history_data: ProjectHistoryCreateEditDTO):
        try:
            updated_project = await self.project_serv.update_project_by_id(project_id, project_data)

            file_data.project_id = project_id
            await self.minio_client.save_file(file_data.model_dump())

            await self.pr_history_serv.add_project_history(project_id, history_data)

            await self.session.commit()
            return updated_project

        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error during project update: {e}")
