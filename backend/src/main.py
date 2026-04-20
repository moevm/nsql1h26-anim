import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router
from database.db import db
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
  print("🚀 App starting...")
  await db.init_db()
  yield
  print("🛑 App shutting down...")
  await db.close()

app = FastAPI(
  lifespan=lifespan,
  version="1.0.0",
  openapi_url="/api/v1/openapi.json",
  docs_url="/api/v1/docs",
)

origins = [
  f'http://{settings.app_react_host}:{settings.app_react_port}',
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host=settings.app_host,
    port=settings.app_port,
    reload=True
  )