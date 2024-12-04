from ..models import User, History
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

class UserRepository():
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_by_id(self, id: int) -> User: 
        query = (
            select(User)
            .options(
                selectinload(User.histories).selectinload(History.project),
                selectinload(User.histories).selectinload(History.file),
            )
            .where(User.id == id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def get_by_email(self, email: str) -> User | None:
        query = (
            select(User)
            .options(
                selectinload(User.histories).selectinload(History.project),
                selectinload(User.histories).selectinload(History.file),
            )
            .where(User.email == email)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def create_user(self, user_data: dict) -> bool:
        try:
            print(user_data)
            new_user = User(**user_data)
            self.session.add(new_user)
            await self.session.flush()  
            await self.session.commit()
            return True
        except:
            await self.session.rollback()
            return False

    async def update_by_id(self, id: int, update_user: dict) -> bool:
        try:
            existing_user = await self.get_by_id(id)
            if not existing_user:
                return False
            for attr, value in update_user.items():
                if value is not None and hasattr(existing_user, attr):
                    setattr(existing_user, attr, value)
            self.session.add(existing_user)
            await self.session.commit()     
            return True
        except:
            await self.session.rollback()
            return False

    async def delete_by_id(self, id: int) -> bool:
        try:
            existing_user = await self.get_by_id(id)
            if not existing_user:
                return False
            await self.session.delete(existing_user)
            await self.session.commit()     
            return True
        except:
            await self.session.rollback()
            return False
