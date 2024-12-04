from ..models import History, Project
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class HistoryRepository():
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_history_by_project(self, project_id: int): 
        hist = await self.session.execute(select(History).filter(History.project_id == project_id))
        return hist.scalars().all()

    async def add_history_to_project(self, project_id: int, history: dict) -> bool:
        try:
            result = await self.session.execute(select(Project).where(Project.id == project_id))
            project = result.scalar_one_or_none()

            if not project:
                raise ValueError(f"Project with id {project_id} not found.")
            
            history = History(project_id=project_id, **history)

            self.session.add(history)
            await self.session.flush()
            await self.session.commit()
            return True
        except:
            await self.session.rollback()
            return False

