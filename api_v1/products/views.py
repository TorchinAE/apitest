from itertools import product

from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.products import crud
from api_v1.products.schemas import ProductCreate, Product
from core.models.db_helper import get_db

products_router = APIRouter(tags=["Products"])


@products_router.get("/", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(get_db)):
    return await crud.get_products(session=session)


@products_router.post("/", response_model=Product)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_product(session=session, product_in=product_in)


@products_router.get("/{product_id}/", response_model=Product)
async def get_products(product_id: int, session: AsyncSession = Depends(get_db)):
    product = await crud.get_product_id(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.http_404_not_found,
        detail=f"Product id {product_id} not found",
    )
