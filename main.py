from contextlib import asynccontextmanager
from core.config import settings
from core.models import Base, db_helper
from fastapi import FastAPI
import uvicorn
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {"message": "Hello World 2"}


@app.get("/hello/")
async def hello(name: str):
    name = name.strip().title()
    return {"message": f"Hello {name}"}


@app.get("/new/")
async def get_items():
    return [
        "item1",
        "item2",
        "item3",
        "item5",
    ]


@app.get("/new/{item_id}")
async def get_item_id(item_id: int):
    return {"item_id": item_id + 50}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
