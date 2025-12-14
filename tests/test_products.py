# tests/test_products.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.products.schemas import ProductCreate
from api_v1.products import crud


@pytest.mark.asyncio
async def test_create_product(async_client: AsyncClient, db_session: AsyncSession):
    product_data = {"name": "Тестовый товар", "price": 99.99}
    response = await async_client.post("/api/v1/products/", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_products(async_client: AsyncClient, db_session: AsyncSession):
    # Предварительно создаём товар через CRUD (или через API)
    product_in = ProductCreate(name="Товар 1", price=10.0)
    await crud.create_product(session=db_session, product_in=product_in)
    await db_session.commit()

    response = await async_client.get("/api/v1/products/")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 1
    assert products[0]["name"] == "Товар 1"
