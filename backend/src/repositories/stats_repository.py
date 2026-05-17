from core.constants import NodeLabels as N, RelationTypes as R

class StatsRepository:
    def __init__(self, db):
        self.db = db

    async def get_posts_stats(
        self,
        x_field: str,
        y_field: str,
        filters: dict,
    ) -> list[dict]:
        where_parts = []
        params = {}

        if filters.get("author"):
            where_parts.append("toLower(u.username) CONTAINS toLower($author)")
            params["author"] = filters["author"]

        if filters.get("type"):
            where_parts.append("p.type = $type")
            params["type"] = filters["type"]

        if filters.get("tag"):
            where_parts.append(f"EXISTS {{ MATCH (p)-[:{R.TAGGED}]->(:{N.TAG} {{name: $tag}}) }}")
            params["tag"] = filters["tag"]

        if filters.get("taxon"):
            where_parts.append(f"EXISTS {{ MATCH (p)-[:{R.OBSERVED}]->(:{N.ANIMAL} {{taxon: $taxon}}) }}")
            params["taxon"] = filters["taxon"]

        where_clause = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""
        x_expr = self._posts_x_expr(x_field)
        
        y_aggregation = {
            "likes_count": "sum(likes_count)",
            "comments_count": "sum(comments_count)",
            "count": "count(DISTINCT p)"
        }.get(y_field, "count(DISTINCT p)")

        query = f"""
            MATCH (u:{N.USER})-[:{R.AUTHORED}]->(p:{N.POST})
            {where_clause}
            OPTIONAL MATCH (p)-[:{R.TAGGED}]->(t:{N.TAG})
            OPTIONAL MATCH (p)-[:{R.OBSERVED}]->(a:{N.ANIMAL})
            OPTIONAL MATCH (:{N.USER})-[lk:{R.LIKED}]->(p)
            OPTIONAL MATCH (c:{N.COMMENT})-[:{R.ON}]->(p)
            WITH p, u, a,
                 collect(DISTINCT t.name) AS tags_list,
                 count(DISTINCT lk) AS likes_count,
                 count(DISTINCT c) AS comments_count
            WITH {x_expr} AS x_val, p, likes_count, comments_count
            WHERE x_val IS NOT NULL
            RETURN x_val AS x, "{y_field}" AS y, {y_aggregation} AS val
            ORDER BY x ASC
        """

        result = await self.db.query(query, params)
        return [{"x": r["x"], "y": r["y"], "count": r["val"]} for r in result]

    def _posts_x_expr(self, field: str) -> str:
        mapping = {
            "type": "p.type",
            "tag": "CASE WHEN size(tags_list) > 0 THEN tags_list[0] ELSE null END",
            "taxon": "a.taxon",
            "author": "u.username",
            "date": "toString(datetime(p.created_at).date)",
        }
        return mapping.get(field, "p.type")

    async def get_users_stats(
        self,
        x_field: str,
        y_field: str,
        filters: dict,
    ) -> list[dict]:
        where_parts = []
        params = {}

        if filters.get("first_name"):
            where_parts.append("toLower(n.first_name) CONTAINS toLower($first_name)")
            params["first_name"] = filters["first_name"]

        if filters.get("last_name"):
            where_parts.append("toLower(n.last_name) CONTAINS toLower($last_name)")
            params["last_name"] = filters["last_name"]

        if filters.get("username"):
            where_parts.append("toLower(n.username) CONTAINS toLower($username)")
            params["username"] = filters["username"]

        if filters.get("role"):
            where_parts.append("n.role = $role")
            params["role"] = filters["role"]

        where_clause = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""
        x_expr = self._users_x_expr(x_field)

        y_aggregation = {
            "followers_count": "sum(followers_count)",
            "following_count": "sum(following_count)",
            "posts_count": "sum(posts_count)",
            "likes_count": "sum(likes_count)",
            "comments_count": "sum(comments_count)",
            "count": "count(DISTINCT x_val)"
        }.get(y_field, "count(DISTINCT x_val)")

        query = f"""
            MATCH (n:{N.USER})
            {where_clause}
            OPTIONAL MATCH (follower:{N.USER})-[r1:{R.FOLLOWED}]->(n)
            OPTIONAL MATCH (n)-[r2:{R.FOLLOWED}]->(following:{N.USER})
            OPTIONAL MATCH (n)-[:{R.AUTHORED}]->(p:{N.POST})
            OPTIONAL MATCH (:{N.USER})-[post_likes:{R.LIKED}]->(p)
            OPTIONAL MATCH (n)-[:{R.AUTHORED}]->(cm:{N.COMMENT})
            WITH n,
                 count(DISTINCT r1) AS followers_count,
                 count(DISTINCT r2) AS following_count,
                 count(DISTINCT p) AS posts_count,
                 count(DISTINCT post_likes) AS likes_count,
                 count(DISTINCT cm) AS comments_count
            WITH {x_expr} AS x_val, followers_count, following_count, posts_count, likes_count, comments_count
            WHERE x_val IS NOT NULL
            RETURN x_val AS x, "{y_field}" AS y, {y_aggregation} AS val
            ORDER BY x ASC
        """

        result = await self.db.query(query, params)
        return [{"x": r["x"], "y": r["y"], "count": r["val"]} for r in result]
    
    def _users_x_expr(self, field: str) -> str:
        mapping = {
            "role": "n.role",
            "username": "n.username",
            "first_name": "n.first_name",
            "last_name": "n.last_name",
            "date": "toString(datetime(n.created_at).date)",
        }
        return mapping.get(field, "n.role")

    async def get_comments_stats(
        self,
        x_field: str,
        y_field: str,
        filters: dict,
    ) -> list[dict]:
        where_parts = []
        params = {}

        if filters.get("author"):
            where_parts.append("toLower(u.username) CONTAINS toLower($author)")
            params["author"] = filters["author"]

        where_clause = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""
        x_expr = self._comments_x_expr(x_field)

        y_aggregation = {
            "likes_count": "sum(likes_count)",
            "count": "count(c)"
        }.get(y_field, "count(c)")

        query = f"""
            MATCH (u:{N.USER})-[:{R.AUTHORED}]->(c:{N.COMMENT})
            {where_clause}
            OPTIONAL MATCH (:{N.USER})-[lk:{R.LIKED}]->(c)
            WITH c, u, count(DISTINCT lk) AS likes_count
            WITH {x_expr} AS x_val, likes_count
            WHERE x_val IS NOT NULL
            RETURN x_val AS x, "{y_field}" AS y, {y_aggregation} AS val
            ORDER BY x ASC
        """

        result = await self.db.query(query, params)
        return [{"x": r["x"], "y": r["y"], "count": r["val"]} for r in result]

    def _comments_x_expr(self, field: str) -> str:
        mapping = {
            "author": "u.username",
            "date": "toString(datetime(c.created_at).date)",
        }
        return mapping.get(field, "u.username")