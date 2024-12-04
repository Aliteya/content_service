from ..repositories import FileRepository, MinioClient
from ..schemas import FileSchema
from sqlalchemy.ext.asyncio import AsyncSession

class FileService():
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
        self.file_repo = FileRepository(self.session)
        self.minio_client = MinioClient(self.session)

    async def add_file(self, file: FileSchema)-> bool:
        file_adding = await self.file_repo.add_file(file.model_dump())
        return file_adding

    async def get_file(self, filename: str) -> FileSchema | None:
        try:
            file = await self.minio_client.get_file_by_filename(filename)
            if not file:
                return None
            return file
        except:
            return None

    async def get_files_by_project(self, project_id: int) -> list[FileSchema]:
        try:
            files = await self.file_repo.get_file_by_project(project_id)
            return files
        except:
            return []

    async def delete_file_filename(self, filename: str) -> bool:
        try:
            result = await self.minio_client.delete_file_by_filename(filename)
            if not result:
                return False
            return result
        except:
            return False
    
    async def delete_file_project(self, project_id: int) -> bool:
        try:
            result = await self.file_repo.delete_files_by_project(project_id)
            if not result:
                return False
            return result
        except:
            return False
    