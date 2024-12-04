from ..repositories import HistoryRepository
from ..schemas import ProjectHistoryCreateEditDTO
from sqlalchemy.ext.asyncio import AsyncSession

class ProjectHistoryService:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
        self.history_repo = HistoryRepository(self.session)

    async def get_project_history(self, project_id: int):
        try:
            print("serv-----------------")
            histories = await self.history_repo.get_history_by_project(project_id)
            print(histories)
            return histories
        except Exception as e:
            print(f"Error fetching project history: {e}")
            return []

    async def add_project_history(self, project_id: int, history_data: ProjectHistoryCreateEditDTO) -> bool:
        try:
            return await self.history_repo.add_history_to_project(project_id, history_data.model_dump())
        except Exception as e:
            print(f"Error adding history: {e}")
            return False
