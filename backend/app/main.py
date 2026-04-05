from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.driver import db
from app.api.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
  await db.connect()
  yield
  await db.close()

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix='/api')
