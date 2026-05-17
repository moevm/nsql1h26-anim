from contextlib import asynccontextmanager

import re
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from neo4j.exceptions import ClientError

from api.router import api_router
from core.config import settings
from core.exceptions import AppException, ConflictException
from database.db import db
from services.system_service import SystemService

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    await SystemService(db).restore_initial_if_empty()
    yield
    await db.close()


app = FastAPI(
    lifespan=lifespan,
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    swagger_ui_parameters={"withCredentials": True},
)

origins = [
    f"http://{settings.app_react_host}:{settings.app_react_port}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status,
        content={
            "error": {
                "code": exc.code,
                "message": exc.detail,
                "context": exc.context
            }
        }
    )


@app.exception_handler(ClientError)
async def neo4j_exception_handler(request: Request, exc: ClientError):
    error_msg = str(exc)
    
    if exc.code == 'Neo.ClientError.Schema.ConstraintValidationFailed':
        match = re.search(r"property\s+`?([a-zA-Z0-9_]+)`?", error_msg)
        
        if match:
            field = match.group(1).replace('_', ' ').title()
            return await app_exception_handler(request, ConflictException(entity=field))
        
        return await app_exception_handler(request, ConflictException(entity="Resource"))

    return await general_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content= {
            "error": {
                "code": "request_validation_error",
                "message": "Invalid Request data",
                "context": {"details": exc.errors()}
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_server_error",
                "message": "An unexpected error occurred",
                "context": {"domain": "server"}
            }
        }
    )


app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.app_host, 
        port=settings.app_port, 
        reload=False
    )
