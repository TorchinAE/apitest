# tests/conftest.py
from typing import AsyncGenerator
import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import text
from core.models import Base
from core.models.db_helper import get_db
from main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Создаём движок — он синхронный, но используется в async-контексте
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False, autocommit=False
)


# ✅ СИНХРОННАЯ фикстура с scope="session"
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Запускаем асинхронную логику через asyncio.run()
    async def _setup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _teardown():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    # Выполняем setup
    asyncio.run(_setup())
    yield
    # Выполняем teardown
    asyncio.run(_teardown())


# Фикстура сессии — остаётся асинхронной
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def override_get_db(db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture
async def async_client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
