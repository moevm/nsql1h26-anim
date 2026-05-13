from core.utils import get_now
from models.base import BaseNode
from schemas.pagination import PaginatedResponse, PaginationParams

class BaseRepository[T: BaseNode]:
    def __init__(self, db, node_label: str, model: type[T]):
        self.db = db
        self.node_label = node_label
        self.model = model


    async def create(self, data: dict) -> T | None:
        query = f"""
            CREATE (n:{self.node_label} $props) 
            RETURN n
        """

        result = await self.db.query(query, parameters={"props": data})
        return self.model.model_validate(result[0]["n"]) if result else None


    async def get_paginated(
        self, 
        params: PaginationParams, 
        match_pattern: str = None, 
        additional_where: str = "", 
        parameters: dict = {}
    ) ->PaginatedResponse[T]:
        parameters.update({
            "limit": params.limit,
            "offset": params.offset
        })

        pattern = match_pattern or f"(n:{self.node_label})"
        
        query = f"""
            MATCH {pattern}
            {additional_where}
            WITH count(n) as total, n
            ORDER BY n.created_at DESC
            SKIP $offset LIMIT $limit
            RETURN collect(n) as items, total
        """

        result = await self.db.query(query, parameters=parameters)
        
        if not result or not result[0]["items"]:
            return PaginatedResponse(
                items=[],
                total=0,
                limit=params.limit,
                offset=params.offset,
                has_more=False
            )

        items = [self.model.model_validate(item) for item in result[0]["items"]]
        total = result[0]["total"]
        
        return PaginatedResponse(
            items=items,
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_more=(params.offset + params.limit) < total
        )

    async def update(self, id: str, data: dict) -> T | None:
        query = f"""
            MATCH (n:{self.node_label} {{id: $id}}) 
            SET n += $props RETURN n
        """

        result = await self.db.query(query, parameters={"id": id, "props": data})
        return self.model.model_validate(result[0]["n"]) if result else None


    async def delete(self, id: str) -> bool:
        query = f"""
            MATCH (n:{self.node_label} {{id: $id}}) 
            DETACH DELETE n RETURN count(*) as count
        """

        result = await self.db.query(query, parameters={"id": id})
        return result[0]["count"] > 0


    async def toggle_relation(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        source_label: str,
        target_label: str
    ) -> bool:
        query = f"""
        MATCH (src:{source_label} {{id: $source_id}})
        MATCH (tgt:{target_label} {{id: $target_id}})
        OPTIONAL MATCH (src)-[r:{rel_type}]->(tgt)
        FOREACH (_ IN CASE WHEN r IS NULL THEN [1] ELSE [] END | CREATE (src)-[:{rel_type}]->(tgt))
        FOREACH (_ IN CASE WHEN r IS NOT NULL THEN [1] ELSE [] END | DELETE r)
        RETURN r IS NULL as created
        """

        result = await self.db.query(query, parameters={
            "source_id": source_id,
            "target_id": target_id
        })
        
        return result[0]["created"]