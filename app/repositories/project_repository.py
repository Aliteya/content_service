from ..models import Project
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class ProjectRepository():
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_by_id(self, id: int) -> Project: 
        user = await self.session.execute(select(Project).filter(Project.id == id))
        return user.scalar_one_or_none()

    async def update_by_id(self, id: int, update_project: dict) -> bool:
        try:
            existing_project = await self.get_by_id(id)
            if not existing_project:
                return False
            for attr, value in update_project.items():
                if value is not None and hasattr(existing_project, attr):
                    setattr(existing_project, attr, value)
            self.session.add(existing_project)
            await self.session.commit()     
            return True
        except:
            await self.session.rollback()
            return False
        
    async def save_project(self, new_project: dict) -> Project | None:
        try:
            save_project = Project(**new_project)
            self.session.add(save_project)
            await self.session.flush()
            await self.session.commit()
            return save_project
        except:
            await self.session.rollback()
            return None

    async def delete_by_id(self, id: int) -> bool:
        try:
            existing_project = await self.get_by_id(id)
            if not existing_project:
                return False
            await self.session.delete(existing_project)
            await self.session.commit()     
            return True
        except:
            await self.session.rollback()
            return False
