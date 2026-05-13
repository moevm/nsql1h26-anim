from repositories.base import BaseRepository
from models.user import User
from core.constants import NodeLabels as N, RelationTypes as R
from schemas.pagination import PaginationParams, PaginatedResponse

class UserRepository(BaseRepository[User]):
    def __init__(self, db):
        super().__init__(db, node_label=N.USER, model=User)

    def _get_base_aggregations(self, current_user_id: str | None = None) -> str:
        user_context = ""
        if current_user_id:
            user_context = f"""
                OPTIONAL MATCH (curr_user:{N.USER} {{id: $current_user_id}})
                OPTIONAL MATCH (curr_user)-[follow_rel:{R.FOLLOWED}]->(n)
            """
        
        return f"""
            OPTIONAL MATCH (follower:{N.USER})-[r1:{R.FOLLOWED}]->(n)
            OPTIONAL MATCH (n)-[r2:{R.FOLLOWED}]->(following:{N.USER})
            OPTIONAL MATCH (n)-[:{R.AUTHORED}]->(p:{N.POST})
            OPTIONAL MATCH (:{N.USER})-[post_likes:{R.LIKED}]->(p)
            OPTIONAL MATCH (n)-[:{R.AUTHORED}]->(c:{N.COMMENT}) 
            {user_context}
            WITH n,
                count(DISTINCT r1) AS followers_count,
                count(DISTINCT r2) AS following_count,
                count(DISTINCT p) AS posts_count,
                count(DISTINCT post_likes) AS likes_count,
                count(DISTINCT c) AS comments_count
                {', follow_rel' if current_user_id else ''}
        """

    def _get_projection(self, current_user_id: str | None = None) -> str:
        followed_proj = "follow_rel IS NOT NULL" if current_user_id else "false"
        
        return f"""
        RETURN n {{
            .*,
            is_followed: {followed_proj},
            followers_count: followers_count,
            following_count: following_count,
            posts_count: posts_count,
            likes_count: likes_count,
            comments_count: comments_count
        }} AS user
        """

    async def get_by_id(self, user_id: str, current_user_id: str | None = None) -> User | None:
        query = f"""
            MATCH (n:{N.USER} {{id: $user_id}})
            {self._get_base_aggregations(current_user_id)}
            {self._get_projection(current_user_id)}
        """

        result = await self.db.query(query, {"user_id": user_id, "current_user_id": current_user_id})
        return self.model.model_validate(result[0]["user"]) if result else None

    async def get_by_identifier(self, identifier: str) -> User | None:
        query = f"""
            MATCH (n:{N.USER})
            WHERE n.email = $identifier OR n.username = $identifier
            RETURN n
        """

        result = await self.db.query(query, {"identifier": identifier})
        return self.model.model_validate(result[0]["n"]) if result else None

    async def list_users(self, params: PaginationParams, current_user_id: str | None = None) -> PaginatedResponse[User]:
        query_params = {
            "limit": params.limit,
            "offset": params.offset,
            "current_user_id": current_user_id
        }
        
        where_clause = ""
        if params.search:
            where_clause = "WHERE n.username =~ $search_regex"
            query_params["search_regex"] = f"(?i).*{params.search}.*"

        count_q = f"MATCH (n:{N.USER}) {where_clause} RETURN count(n) as total"
        count_res = await self.db.query(count_q, query_params)
        total = count_res[0]["total"] if count_res else 0

        if total == 0:
            return PaginatedResponse(items=[], total=0, limit=params.limit, offset=params.offset, has_more=False)

        query = f"""
            MATCH (n:{N.USER})
            {where_clause}
            ORDER BY n.username ASC
            SKIP $offset
            LIMIT $limit
            {self._get_base_aggregations(current_user_id)}
            {self._get_projection(current_user_id)}
        """
        
        results = await self.db.query(query, query_params)
        items = [self.model.model_validate(r["user"]) for r in results]

        return PaginatedResponse(
            items=items,
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_more=total > (params.offset + params.limit)
        )

    async def toggle_follow(self, user_id: str, target_id: str) -> bool:
        return await self.toggle_relation(
            source_id=user_id, 
            target_id=target_id, 
            rel_type=R.FOLLOWED, 
            source_label=N.USER, 
            target_label=N.USER
        )
    
    async def get_followers(self, user_id: str, current_user_id: str | None = None) -> PaginatedResponse[User]:
        query = f"""
            MATCH (follower:{N.USER})-[:{R.FOLLOWED}]->(n:{N.USER} {{id: $user_id}})
            WITH follower AS n
            {self._get_base_aggregations(current_user_id)}
            {self._get_projection(current_user_id)}
        """
        results = await self.db.query(query, {"user_id": user_id, "current_user_id": current_user_id})
        items = [self.model.model_validate(r["user"]) for r in results]
        return PaginatedResponse(items=items, total=len(items), limit=100, offset=0, has_more=False)


    async def get_following(self, user_id: str, current_user_id: str | None = None) -> PaginatedResponse[User]:
        query = f"""
            MATCH (n:{N.USER} {{id: $user_id}})-[:{R.FOLLOWED}]->(following:{N.USER})
            WITH following AS n
            {self._get_base_aggregations(current_user_id)}
            {self._get_projection(current_user_id)}
        """
        results = await self.db.query(query, {"user_id": user_id, "current_user_id": current_user_id})
        items = [self.model.model_validate(r["user"]) for r in results]
        return PaginatedResponse(items=items, total=len(items), limit=100, offset=0, has_more=False)