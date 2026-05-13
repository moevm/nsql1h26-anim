from repositories.base import BaseRepository
from models.animal import Animal
from schemas.pagination import AnimalPaginationParams, PaginatedResponse
from core.constants import NodeLabels as N, RelationTypes as R

class AnimalRepository(BaseRepository[Animal]):
    def __init__(self, db):
        super().__init__(db, N.ANIMAL, Animal)
    
    async def get_by_scientific_name(self, scientific_name: str) -> Animal | None:
        query = f"""
            MATCH (n:{N.ANIMAL} {{scientific_name: $scientific_name}}) 
            RETURN n 
        """

        result = await self.db.query(query, parameters={"scientific_name": scientific_name})
        return self.model.model_validate(result[0]["n"]) if result else None
    
    async def list_animals(self, params: AnimalPaginationParams) -> list[PaginatedResponse[Animal]]:
        filters = []
        cypher_params = {}

        if params.taxon:
            filters.append("n.taxon = $taxon")
            cypher_params["taxon"] = params.taxon

        if params.search:
            cypher_params["search_regex"] = f"(?i).*{params.search}.*"
            filters.append("(n.name =~ $search_regex OR n.scientific_name =~ $search_regex)")

        where_clause = "WHERE " + " AND ".join(filters) if filters else ""

        return await self.get_paginated(
            params=params,
            additional_where=where_clause,
            parameters=cypher_params
        )