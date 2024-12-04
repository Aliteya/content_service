from ..models import File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class MinioClient():
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def save_file(self, file: dict) -> bool:
        try:
            file = File(**file)
            self.session.add(file)
            await self.session.flush()
            await self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    async def get_file_by_filename(self, name) -> File:
        file = await self.session.execute(select(File).filter(File.name == name))
        return file.scalar_one_or_none()

    async def delete_file_by_filename(self, name) -> bool:
        try:
            existing_file = await self.get_file_by_filename(name)
            if not existing_file:
                return False
            await self.session.delete(existing_file)
            await self.session.commit()     
            return True
        except:
            await self.session.rollback()
            return False