from fastapi import APIRouter
from api.user.user import user_router


router = APIRouter()
router.include_router(user_router, prefix="/users")


__all__ = ["router"]
