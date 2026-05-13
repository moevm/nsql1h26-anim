from fastapi import APIRouter
from services.system_service import SystemService
from database.db import db

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/export")
async def export_database():
    service = SystemService(db)
    return await service.export_all_data()


@router.post("/import", status_code=200)
async def import_database():
    service = SystemService(db)
    await service.import_from_file()
    return {"status": "success"}