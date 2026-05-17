from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from services.system_service import SystemService
from database.db import db
from core.constants import SystemConst
from core.utils import get_now

router = APIRouter(prefix="/system", tags=["system"])

ALLOWED_CONTENT_TYPES = {"application/json", "text/plain"}
MAX_UPLOAD_BYTES = SystemConst.MAX_IMPORT_FILE_BYTES


@router.get(
    "/export",
    response_class=Response,
    responses={200: {"content": {"application/json": {}}}},
)
async def export_database():
    service = SystemService(db)
    content = await service.export_all_data()

    filename = f"db_export_{get_now().strftime('%Y%m%d_%H%M%S')}.json"

    return Response(
        content=content,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(content)),
        },
    )


@router.post(
    "/import",
    status_code=200,
)
async def import_database(file: UploadFile = File(...)):
    ct = (file.content_type or "").split(";")[0].strip()
    if ct and ct not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Недопустимый тип файла: {ct}. Ожидается application/json",
        )

    if not file.filename or not file.filename.lower().endswith(".json"):
        raise HTTPException(
            status_code=415,
            detail="Файл должен иметь расширение .json",
        )

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Файл слишком большой (максимум 100 МБ)",
        )

    service = SystemService(db)
    await service.import_from_uploaded_file(content)
    return {
        "status": "success", 
        "message": "База данных успешно импортирована"
    }