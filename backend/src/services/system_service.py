import json
import os
from pathlib import Path
from typing import Any
from datetime import datetime, date
from neo4j.time import DateTime, Date, Time, Duration
from database.db import Neo4jDatabase
from core.exceptions import AppException

BACKUP_DIR  = Path("backups")
BACKUP_FILE = BACKUP_DIR / "backup.json"


class Neo4jEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (DateTime, datetime)):
            return obj.isoformat()
        if isinstance(obj, (Date, date)):
            return obj.isoformat()
        if isinstance(obj, Time):
            return str(obj)
        if isinstance(obj, Duration):
            return str(obj)
        return super().default(obj)


class SystemService:
    def __init__(self, db: Neo4jDatabase):
        self.db = db

    async def export_all_data(self) -> dict[str, Any]:
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
            "nodes":         [r["node"] for r in nodes_res],
            "relationships": [r["rel"]  for r in rels_res],
        }

        BACKUP_DIR.mkdir(exist_ok=True)
        with open(BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, cls=Neo4jEncoder)

        return json.loads(json.dumps(data, cls=Neo4jEncoder))

    async def import_from_file(self) -> None:
        if not BACKUP_FILE.exists():
            raise AppException(
                detail=f"Файл {BACKUP_FILE} не найден",
                code="backup_not_found",
                status=404,
            )

        with open(BACKUP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        await self.import_all_data(data)

    async def import_all_data(self, data: dict) -> None:
        nodes = data.get("nodes", [])
        rels  = data.get("relationships", [])

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

    async def restore_if_empty(self) -> bool:
        result = await self.db.query("MATCH (n) RETURN count(n) AS cnt")
        count  = result[0]["cnt"]

        if count > 0:
            return False

        if not BACKUP_FILE.exists():
            return False

        with open(BACKUP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        await self.import_all_data(data)
        print(f"Base read from {BACKUP_FILE}")
        return True