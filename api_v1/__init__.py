from fastapi import APIRouter

from api_v1.users.views import users_router
from api_v1.products.views import products_router

router = APIRouter()
router.include_router(router=products_router, prefix="/products")
router.include_router(router=users_router, prefix="/users")
