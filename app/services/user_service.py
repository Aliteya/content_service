from ..repositories import UserRepository
from ..schemas import UserCreateEditDTO, UserReadDTO, ProjectReadDTO, ProjectHistoryReadDTO
from sqlalchemy.ext.asyncio import AsyncSession

class UserService():
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
        self.user_repo = UserRepository(self.session)

    async def create_new_user(self, user: UserCreateEditDTO) -> bool:
        creation = await self.user_repo.create_user(user.model_dump())
        return creation
    
    async def get_user_by_id(self, id: int) -> UserReadDTO | None:
        user = await self.user_repo.get_by_id(id)
        if not user:
            return None 
        project_map = {}
        for history in user.histories:
            if history.project_id not in project_map:
                project_map[history.project_id] = ProjectReadDTO(
                    id=history.project.id,
                    projectName=history.project.projectName,
                    category=history.project.category,
                    my_histories=[],
                )
        
            project_map[history.project_id].my_histories.append(
                ProjectHistoryReadDTO(
                    project_id=history.project.id,
                    type=history.type, 
                    fileName=history.file.name,
                    filter=history.filter,
                    startTime=history.startTime.isoformat(),
                    endTime=history.endTime.isoformat(),
                )
            )
        return UserReadDTO(
            id = id,
            fullName=user.fullName,
            my_projects=list(project_map.values()),
        )
    
    async def get_user_by_email(self, email: str) -> UserReadDTO | None:
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None 
        project_map = {}
        for history in user.histories:
            if history.project_id not in project_map:
                project_map[history.project_id] = ProjectReadDTO(
                    id=history.project.id,
                    projectName=history.project.projectName,
                    category=history.project.category,
                    my_histories=[],
                )
        
            project_map[history.project_id].my_histories.append(
                ProjectHistoryReadDTO(
                    project_id=history.project.id,
                    type=history.type, 
                    fileName=history.file.name,
                    filter=history.filter,
                    startTime=history.startTime.isoformat(),
                    endTime=history.endTime.isoformat(),
                )
            )
        return UserReadDTO(
            id = user.id,
            fullName=user.fullName,
            my_projects=list(project_map.values()),
        )
    
    async def update_user_by_id(self, id: int, old_user: UserCreateEditDTO) -> bool:
        updating = await self.user_repo.update_by_id(id, old_user.model_dump())
        return updating

    async def delete_user_by_id(self, id: int) -> bool:
        deletion = await self.user_repo.delete_by_id(id)
        return deletion
    
    
