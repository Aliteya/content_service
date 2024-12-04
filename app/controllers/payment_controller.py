from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import SubscriptionType
from app.database import get_session
from ..services import PaymentService

payment_router = APIRouter(prefix="/payment",tags=["payment"])

def get_payment_service(session: AsyncSession = Depends(get_session)) -> PaymentService:
    return PaymentService(session)


@payment_router.post("/subscribe/{user_id}")
async def subscribe_user(user_id: int, subscription: SubscriptionType, 
    payment_service: PaymentService = Depends(get_payment_service)):
    success = await payment_service.process_subscription(subscription, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid subscription type")
    return {"message": f"Subscription '{subscription}' processed for user {user_id}"}


@payment_router.get("/check/{user_id}")
async def check_user_subscription(user_id: int, 
    payment_service: PaymentService = Depends(get_payment_service)):

    expiration = await payment_service.check_subscription_expiration(user_id)
    if expiration is None:
        return {"user_id": user_id, "status": "No active subscription"}
    return {"user_id": user_id, "payment_status": expiration}

