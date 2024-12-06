from ..models import File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

class FileRepository():
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
    
    async def add_file(self, file: dict) -> File| None:
        try:
            file = File(**file)
            self.session.add(file)
            await self.session.flush()
            await self.session.commit()
            return file
        except:
            await self.session.rollback()
            return None

    async def get_file_by_project(self, project_id) :
        file = await self.session.execute(select(File).filter(File.project_id == project_id))
        return file.scalars().all()
    
    async def delete_files_by_project(self, project_id) -> bool:
        try:
            existing_files = await self.get_file_by_project(project_id)
            if not existing_files:
                return False
            else: 
                for file in existing_files:
                    await self.session.delete(file)
            await self.session.commit()     
            return True
        except:
            await self.session.rollback()
            return False