from ..repositories import UserRepository
from ..models import SubscriptionType
from sqlalchemy.ext.asyncio import AsyncSession

#это костыль потому что в диаграмме не было нормально реализована система подписки,
#  пришлось ее частично из головы брать а времени еще одну бд подвязывать нет, так что не
# судите строго , изобретаю велосипед

class PaymentService():
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
        self.user_repo = UserRepository(self.session)

    async def process_subscription(self, subscription: SubscriptionType, user_id: int) -> bool:
        cool = 0
        if subscription.value == "GOLD":
            cool+=10
        elif subscription.value == "PLATINUM":
            cool += 20
        elif subscription.value == "UNLIMITED":
            cool += 100
        else: 
            return False
        note = await self.edit_subscription(subscription, user_id, cool)
        return note
    
    async def check_subscription_expiration(self, user_id: int) -> None:
        try:
            user = await self.user_repo.get_by_id(user_id)        
            return user.subscription
        except:
            return None
        
    async def edit_subscription(self, subscription: SubscriptionType, user_id: int, cool: int) -> bool:
        note = await self.user_repo.update_by_id(user_id, {"subscription": subscription.value})
        return note
