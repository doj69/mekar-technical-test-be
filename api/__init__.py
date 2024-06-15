from fastapi import APIRouter

from api import user

router_v1 = APIRouter(prefix="/api/v1")
router_v1.include_router(user.router)

__all__ = ["router_v1"]
