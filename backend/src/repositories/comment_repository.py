from repositories.base import BaseRepository
from models.comment import CommentTree
from schemas.pagination import PaginationParams, PaginatedResponse
from core.constants import NodeLabels as N, RelationTypes as R


class CommentRepository(BaseRepository[CommentTree]):
    def __init__(self, db):
        super().__init__(db, node_label=N.COMMENT, model=CommentTree)

    async def create_comment(
        self,
        props: dict,
        author_id: str,
        post_id: str,
        parent_id: str | None = None,
    ) -> CommentTree:
        query = f"""
            MATCH (u:{N.USER} {{id: $author_id}})
            MATCH (p:{N.POST} {{id: $post_id}})
            CREATE (c:{N.COMMENT} $props)
            CREATE (u)-[:{R.AUTHORED}]->(c)
            CREATE (c)-[:{R.ON}]->(p)
        """
        params = {"author_id": author_id, "post_id": post_id, "props": props}

        if parent_id:
            query += f"""
                WITH c, u
                MATCH (parent:{N.COMMENT} {{id: $parent_id}})
                CREATE (c)-[:{R.REPLIED_TO}]->(parent)
            """
            params["parent_id"] = parent_id

        query += f"""
        WITH c, u
        OPTIONAL MATCH (c)-[:{R.REPLIED_TO}]->(parent:{N.COMMENT})
        RETURN c {{
            .*,
            author: u {{ .* }},
            likes_count: 0,
            is_liked: false,
            parent_id: parent.id,
            replies: []
        }} AS comment
        """
        result = await self.db.query(query, params)
        return self.model.model_validate(result[0]["comment"])

    async def get_comments_tree(
        self,
        post_id: str,
        params: PaginationParams,
        current_user_id: str | None = None
    ) -> PaginatedResponse[CommentTree]:
        query_params = {
            "post_id": post_id,
            "offset": params.offset,
            "limit": params.limit,
            "me": current_user_id
        }

        query = f"""
            MATCH (p:{N.POST} {{id: $post_id}})<-[:{R.ON}]-(n:{N.COMMENT})
            WHERE NOT (n)-[:{R.REPLIED_TO}]->(:{N.COMMENT})
            
            WITH count(n) as total_count, n
            ORDER BY n.created_at ASC
            SKIP $offset LIMIT $limit

            MATCH (author:{N.USER})-[:{R.AUTHORED}]->(n)
            OPTIONAL MATCH (:{N.USER})-[all_likes:{R.LIKED}]->(n)
            OPTIONAL MATCH (curr_user:{N.USER} {{id: $me}})-[liked_rel:{R.LIKED}]->(n)
            
            WITH n, total_count, author, 
                 count(DISTINCT all_likes) as n_likes, 
                 liked_rel IS NOT NULL as n_liked_by_me

            OPTIONAL MATCH (reply:{N.COMMENT})-[:{R.REPLIED_TO}]->(n)
            OPTIONAL MATCH (reply_author:{N.USER})-[:{R.AUTHORED}]->(reply)
            
            WITH n, total_count, author, n_likes, n_liked_by_me, reply, reply_author
            ORDER BY reply.created_at ASC

            WITH n, total_count, author, n_likes, n_liked_by_me,
                collect(CASE WHEN reply IS NOT NULL THEN reply {{ 
                    .*, 
                    author: reply_author {{ .* }},
                    replies: [], 
                    likes_count: 0, 
                    is_liked: false 
                }} END) as replies_data

            RETURN n {{
                .*,
                author: author {{ .* }},
                likes_count: n_likes,
                is_liked: n_liked_by_me,
                replies: replies_data
            }} as comment_data, total_count as total
        """
        result = await self.db.query(query, query_params)
        
        if not result:
            return PaginatedResponse(
                items=[], 
                total=0, 
                limit=params.limit, 
                offset=params.offset, 
                has_more=False
            )

        items = [self.model.model_validate(res["comment_data"]) for res in result]
        total = result[0]["total"]

        return PaginatedResponse(
            items=items,
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_more=(params.offset + params.limit) < total
        )

    
    async def update_comment(
        self,
        comment_id: str,
        props: dict,
        current_user_id: str,
    ) -> CommentTree | None:
        query = f"""
            MATCH (u:{N.USER} {{id: $user_id}})-[:{R.AUTHORED}]->(c:{N.COMMENT} {{id: $comment_id}})
            SET c += $props
            WITH c, u
            OPTIONAL MATCH (:{N.USER})-[all_likes:{R.LIKED}]->(c)
            OPTIONAL MATCH (curr_user:{N.USER} {{id: $user_id}})-[liked_rel:{R.LIKED}]->(c)
            WITH c, u,
                count(DISTINCT all_likes) AS likes_count,
                liked_rel IS NOT NULL AS is_liked
            RETURN c {{
                .*,
                author: u {{ .* }},
                likes_count: likes_count,
                is_liked: is_liked,
                replies: []
            }} AS comment
        """

        result = await self.db.query(query, {
            "user_id": current_user_id,
            "comment_id": comment_id,
            "props": props
        })

        return self.model.model_validate(result[0]["comment"]) if result else None

    async def delete_comment_safe(self, comment_id: str, current_user_id: str) -> bool:
        query = f"""
            MATCH (u:{N.USER} {{id: $user_id}})-[:{R.AUTHORED}]->(c:{N.COMMENT} {{id: $comment_id}})
            OPTIONAL MATCH (child:{N.COMMENT})-[:{R.REPLIED_TO}*]->(c)
            DETACH DELETE c, child
            RETURN count(c) as deleted
        """

        result = await self.db.query(query, {"user_id": current_user_id, "comment_id": comment_id})
        return result[0]["deleted"] > 0

    async def toggle_like(self, comment_id: str, user_id: str) -> bool:
        return await self.toggle_relation(
            user_id, 
            comment_id, 
            R.LIKED, 
            N.USER, 
            N.COMMENT
        )
    

    async def toggle_like(self, comment_id: str, user_id: str) -> bool:
        return await self.toggle_relation(user_id, comment_id, R.LIKED, N.USER, N.COMMENT)