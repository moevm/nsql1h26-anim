import json
from pathlib import Path
from datetime import datetime, date
from neo4j.time import DateTime, Date, Time, Duration
from neo4j.spatial import Point
from database.db import Neo4jDatabase
from core.constants import SystemConst
from core.exceptions import AppException
from core.utils import get_now

INITIAL_BACKUP_FILE = Path("backups") / "initial_db.json"
REQUIRED_KEYS = {"nodes", "relationships"}


def _neo4j_to_python(obj):
    if isinstance(obj, dict):
        return {k: _neo4j_to_python(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_neo4j_to_python(i) for i in obj]
    if isinstance(obj, (DateTime, datetime)):
        return obj.isoformat()
    if isinstance(obj, (Date, date)):
        return obj.isoformat()
    if isinstance(obj, Time):
        return str(obj)
    if isinstance(obj, Duration):
        return str(obj)
    if isinstance(obj, Point):
        return {"x": obj.x, "y": obj.y, "z": getattr(obj, "z", None), "srid": obj.srid}
    return obj


def _validate_backup_structure(data: dict) -> None:
    if not isinstance(data, dict):
        raise AppException(
            detail="Неверный формат файла: ожидается JSON-объект",
            code="invalid_backup_format",
            status=422,
        )
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise AppException(
            detail=f"Неверный формат файла: отсутствуют поля {missing}",
            code="invalid_backup_format",
            status=422,
        )
    if not isinstance(data["nodes"], list):
        raise AppException(
            detail="Неверный формат файла: 'nodes' должен быть массивом",
            code="invalid_backup_format",
            status=422,
        )
    if not isinstance(data["relationships"], list):
        raise AppException(
            detail="Неверный формат файла: 'relationships' должен быть массивом",
            code="invalid_backup_format",
            status=422,
        )


class SystemService:
    def __init__(self, db: Neo4jDatabase):
        self.db = db

    async def export_all_data(self) -> bytes:
        nodes_res = await self.db.query("""
            MATCH (n)
            RETURN {
                id: id(n),
                labels: labels(n),
                properties: properties(n)
            } AS node
        """)
        rels_res = await self.db.query("""
            MATCH (s)-[r]->(e)
            RETURN {
                start_node_id: id(s),
                end_node_id:   id(e),
                type:          type(r),
                properties:    properties(r)
            } AS rel
        """)

        data = {
            "exported_at": get_now().isoformat(),
            "nodes": [_neo4j_to_python(r["node"]) for r in nodes_res],
            "relationships": [_neo4j_to_python(r["rel"]) for r in rels_res],
        }

        return json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")

    async def import_from_uploaded_file(self, content: bytes) -> None:
        if len(content) > SystemConst.MAX_IMPORT_FILE_BYTES:
            raise AppException(
                detail="Файл слишком большой (максимум 1000 МБ)",
                code="file_too_large",
                status=413,
            )

        try:
            data = json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AppException(
                detail=f"Файл не является валидным JSON: {exc}",
                code="invalid_json",
                status=422,
            )

        _validate_backup_structure(data)
        await self._import_data(data)

    async def _import_data(self, data: dict) -> None:
        nodes = data.get("nodes", [])
        rels = data.get("relationships", [])

        async with await self.db.get_session() as session:
            async with await session.begin_transaction() as tx:
                await tx.run("MATCH (n) DETACH DELETE n")

                await tx.run("""
                    UNWIND $nodes AS nd
                    CALL apoc.create.node(nd.labels, nd.properties) YIELD node
                    SET node.__import_id = nd.id
                """, nodes=nodes)

                await tx.run("""
                    UNWIND $rels AS rd
                    MATCH (s {__import_id: rd.start_node_id})
                    MATCH (e {__import_id: rd.end_node_id})
                    CALL apoc.create.relationship(s, rd.type, rd.properties, e) YIELD rel
                    RETURN count(rel)
                """, rels=rels)

                await tx.run("MATCH (n) REMOVE n.__import_id")
                await tx.commit()

    async def restore_initial_if_empty(self) -> bool:
        result = await self.db.query("MATCH (n) RETURN count(n) AS cnt")
        if result[0]["cnt"] > 0:
            return False

        if not INITIAL_BACKUP_FILE.exists():
            return False

        with open(INITIAL_BACKUP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        _validate_backup_structure(data)
        await self._import_data(data)
        return True