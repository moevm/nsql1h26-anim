from repositories.base import BaseRepository
from models.post import PostBase
from core.utils import generate_uid
from core.constants import NodeLabels as N, RelationTypes as R
from schemas.pagination import PostPaginationParams, PaginatedResponse

class PostRepository(BaseRepository[PostBase]):
    def __init__(self, db):
        super().__init__(db, node_label=N.POST, model=PostBase)

    def _get_projection(self, current_user_id: str | None = None) -> str:
        liked_proj = "liked_rel IS NOT NULL" if current_user_id else "false"
        followed_proj = "follow_rel IS NOT NULL" if current_user_id else "false"
        return f"""
        RETURN p {{
            .*,
            author: u {{ .*, is_followed: {followed_proj} }},
            animal: a {{ .* }},
            tags: tags_list,
            is_liked: {liked_proj},
            likes_count: likes_count,
            comments_count: comments_count
        }} AS post
        """

    def _get_base_aggregations(self, current_user_id: str | None = None) -> str:
        user_context = ""
        if current_user_id:
            user_context = f"""
                OPTIONAL MATCH (curr_user:{N.USER} {{id: $current_user_id}})
                OPTIONAL MATCH (curr_user)-[liked_rel:{R.LIKED}]->(p)
                OPTIONAL MATCH (curr_user)-[follow_rel:{R.FOLLOWED}]->(u)
            """
        return f"""
            OPTIONAL MATCH (p)-[:{R.TAGGED}]->(t:{N.TAG})
            OPTIONAL MATCH (p)-[:{R.OBSERVED}]->(a:{N.ANIMAL})
            OPTIONAL MATCH (:{N.USER})-[all_likes:{R.LIKED}]->(p)
            OPTIONAL MATCH (p)<-[:{R.ON}]-(c:{N.COMMENT})
            {user_context}
            WITH p, u, a, 
                collect(DISTINCT t.name) AS tags_list,
                count(DISTINCT all_likes) AS likes_count,
                count(DISTINCT c) AS comments_count
                {', liked_rel, follow_rel' if current_user_id else ''}
        """

    async def get_feed(self, params: PostPaginationParams, current_user_id: str | None = None) -> PaginatedResponse[PostBase]:
        query_params = {
            "current_user_id": current_user_id,
            "limit": params.limit,
            "offset": params.offset
        }

        matches = [f"(u:{N.USER})-[:{R.AUTHORED}]->(p:{N.POST})"]
        where = []

        if params.only_followed and current_user_id:
            matches.append(f"(:{N.USER} {{id: $current_user_id}})-[:{R.FOLLOWED}]->(u)")

        if params.tag:
            matches.append(f"(p)-[:{R.TAGGED}]->(:{N.TAG} {{name: $tag}})")
            query_params["tag"] = params.tag

        need_animal_match = params.taxon or params.scientific_name
        if need_animal_match:
            matches.append(f"(p)-[:{R.OBSERVED}]->(a_filter:{N.ANIMAL})")
            if params.taxon:
                where.append("toLower(a_filter.taxon) = toLower($taxon)")
                query_params["taxon"] = params.taxon
            if params.scientific_name:
                where.append("toLower(a_filter.scientific_name) CONTAINS toLower($scientific_name)")
                query_params["scientific_name"] = params.scientific_name

        if params.search:
            where.append("(toLower(p.title) CONTAINS toLower($search) OR toLower(p.content) CONTAINS toLower($search))")
            query_params["search"] = params.search

        if params.author:
            where.append("(toLower(u.id) = toLower($author) OR toLower(u.username) CONTAINS toLower($author))")
            query_params["author"] = params.author

        match_str = "MATCH " + ", ".join(matches)
        where_str = "WHERE " + " AND ".join(where) if where else ""

        count_q = f"{match_str} {where_str} RETURN count(DISTINCT p) as total"
        count_res = await self.db.query(count_q, query_params)
        total = count_res[0]["total"] if count_res else 0

        if total == 0:
            return PaginatedResponse(items=[], total=0, limit=params.limit, offset=params.offset, has_more=False)

        order_col = "likes_count" if params.sort == "popular" else "p.created_at"
        if params.sort == "oldest":
            order_dir = "ASC"
        else:
            order_dir = "DESC"

        main_q = f"""
            {match_str}
            {where_str}
            WITH DISTINCT p, u
            {self._get_base_aggregations(current_user_id)}
            ORDER BY {order_col} {order_dir}
            SKIP $offset
            LIMIT $limit
            {self._get_projection(current_user_id)}
        """

        results = await self.db.query(main_q, query_params)
        items = [self.model.model_validate(r["post"]) for r in results]

        return PaginatedResponse(
            items=items,
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_more=total > (params.offset + params.limit)
        )

    async def get_post(self, post_id: str, current_user_id: str | None = None) -> PostBase | None:
        query = f"""
            MATCH (u:{N.USER})-[:{R.AUTHORED}]->(p:{N.POST} {{id: $post_id}})
            
            OPTIONAL MATCH (p)-[:{R.TAGGED}]->(t:{N.TAG})
            OPTIONAL MATCH (p)-[:{R.OBSERVED}]->(a:{N.ANIMAL})
            OPTIONAL MATCH (:{N.USER})-[all_p_likes:{R.LIKED}]->(p)
            OPTIONAL MATCH (curr_u:{N.USER} {{id: $current_user_id}})
            OPTIONAL MATCH (curr_u)-[p_liked_rel:{R.LIKED}]->(p)
            OPTIONAL MATCH (curr_u)-[follow_rel:{R.FOLLOWED}]->(u)
            
            WITH p, u, a, 
                collect(DISTINCT t.name) AS tags_list,
                count(DISTINCT all_p_likes) AS p_likes_count,
                p_liked_rel IS NOT NULL AS p_is_liked,
                follow_rel IS NOT NULL AS u_is_followed
                
            OPTIONAL MATCH (all_c:{N.COMMENT})-[:{R.ON}]->(p)
            WITH p, u, a, tags_list, p_likes_count, p_is_liked, u_is_followed, 
                count(DISTINCT all_c) as total_comments_count

            OPTIONAL MATCH (c:{N.COMMENT})-[:{R.ON}]->(p)
            WHERE NOT (c)-[:{R.REPLIED_TO}]->()
            
            OPTIONAL MATCH (c_author:{N.USER})-[:{R.AUTHORED}]->(c)
            OPTIONAL MATCH (:{N.USER})-[cl:{R.LIKED}]->(c)
            OPTIONAL MATCH (curr_u2:{N.USER} {{id: $current_user_id}})-[cl_me:{R.LIKED}]->(c)
            
            WITH p, u, a, tags_list, p_likes_count, p_is_liked, u_is_followed, total_comments_count,
                c, c_author, 
                count(DISTINCT cl) as c_likes, 
                cl_me IS NOT NULL as c_is_liked
            ORDER BY c.created_at DESC
            
            OPTIONAL MATCH (rep:{N.COMMENT})-[:{R.REPLIED_TO}]->(c)
            OPTIONAL MATCH (rep_auth:{N.USER})-[:{R.AUTHORED}]->(rep)
            
            WITH p, u, a, tags_list, p_likes_count, p_is_liked, u_is_followed, total_comments_count,
                c, c_author, c_likes, c_is_liked, rep, rep_auth
            ORDER BY rep.created_at ASC
            
            WITH p, u, a, tags_list, p_likes_count, p_is_liked, u_is_followed, total_comments_count,
                c, c_author, c_likes, c_is_liked,
                collect(CASE WHEN rep IS NOT NULL THEN rep {{
                    .*,
                    author: rep_auth {{ .* }},
                    replies: [],
                    likes_count: 0,
                    is_liked: false
                }} END) as reps_data
                
            WITH p, u, a, tags_list, p_likes_count, p_is_liked, u_is_followed, total_comments_count,
                collect(CASE WHEN c IS NOT NULL THEN c {{
                    .*,
                    author: c_author {{ .* }},
                    likes_count: c_likes,
                    is_liked: c_is_liked,
                    replies: reps_data
                }} END) as comments_list

            RETURN p {{
                .*,
                author: u {{ .*, is_followed: u_is_followed }},
                animal: a {{ .* }},
                tags: tags_list,
                is_liked: p_is_liked,
                likes_count: p_likes_count,
                comments_count: total_comments_count,
                comments: comments_list
            }} AS post
        """
        
        params = {"post_id": post_id, "current_user_id": current_user_id}
        result = await self.db.query(query, params)
        
        if not result or not result[0].get("post"):
            return None

        return self.model.model_validate(result[0]["post"])

    async def create_post(self, props: dict, author_id: str, tags: list[str] = None, animal_props: dict = None) -> PostBase:
        query = f"""
            MATCH (u:{N.USER} {{id: $author_id}})
            CREATE (p:{N.POST} $props)
            CREATE (u)-[:{R.AUTHORED}]->(p)
            WITH p, u
        """
        params = {"author_id": author_id, "props": props}
        if animal_props:
            query += f"""
                MERGE (a:{N.ANIMAL} {{scientific_name: $animal_props.scientific_name}})
                ON CREATE SET a = $animal_props, a.id = $animal_id
                MERGE (p)-[:{R.OBSERVED}]->(a)
                WITH p, u, a
            """
            params.update({"animal_props": animal_props, "animal_id": generate_uid()})
        else:
            query += " WITH p, u, null AS a "
        if tags:
            query += f"""
                UNWIND $tags AS t_name
                MERGE (t:{N.TAG} {{name: t_name}})
                MERGE (p)-[:{R.TAGGED}]->(t)
                WITH p, u, a
            """
            params["tags"] = tags
        query += f" {self._get_base_aggregations(author_id)} {self._get_projection(author_id)}"
        params["current_user_id"] = author_id
        result = await self.db.query(query, params)
        return self.model.model_validate(result[0]["post"])


    async def update_post_safe(self, post_id: str, props: dict, current_user_id: str, tags: list[str] | None = None, animal_props: dict | None = None, detach_animal: bool = False) -> PostBase | None:
        query = f"""
            MATCH (u:{N.USER} {{id: $current_user_id}})-[:{R.AUTHORED}]->(p:{N.POST} {{id: $post_id}})
            SET p += $props
            WITH p, u
        """
        params = {"post_id": post_id, "current_user_id": current_user_id, "props": props}

        if tags is not None:
            query += f"""
                OPTIONAL MATCH (p)-[old_tag:{R.TAGGED}]->()
                DELETE old_tag
                WITH p, u
                UNWIND $tags AS t_name
                MERGE (t:{N.TAG} {{name: t_name}})
                MERGE (p)-[:{R.TAGGED}]->(t)
                WITH p, u
            """
            params["tags"] = tags

        if detach_animal:
            query += f"""
                OPTIONAL MATCH (p)-[obs:{R.OBSERVED}]->()
                DELETE obs
                WITH p, u
            """
        elif animal_props is not None:
            query += f"""
                OPTIONAL MATCH (p)-[:{R.OBSERVED}]->(old_a:{N.ANIMAL})
                FOREACH (_ IN CASE WHEN old_a IS NOT NULL THEN [1] ELSE [] END |
                    SET old_a += $animal_props
                )
                WITH p, u, old_a
                FOREACH (_ IN CASE WHEN old_a IS NULL THEN [1] ELSE [] END |
                    MERGE (new_a:{N.ANIMAL} {{scientific_name: $animal_props.scientific_name}})
                    ON CREATE SET new_a = $animal_props, new_a.id = $animal_id
                    MERGE (p)-[:{R.OBSERVED}]->(new_a)
                )
                WITH p, u
            """
            params["animal_props"] = animal_props
            params["animal_id"] = generate_uid()

        query += f" WITH p, u, null AS a {self._get_base_aggregations(current_user_id)} {self._get_projection(current_user_id)}"

        result = await self.db.query(query, params)
        return self.model.model_validate(result[0]["post"]) if result else None

    async def delete_post_safe(self, post_id: str, current_user_id: str) -> bool:
        query = f"""
            MATCH (u:{N.USER} {{id: $current_user_id}})-[:{R.AUTHORED}]->(p:{N.POST} {{id: $post_id}})
            OPTIONAL MATCH (c:{N.COMMENT})-[:{R.ON}]->(p)
            OPTIONAL MATCH (child:{N.COMMENT})-[:{R.REPLIED_TO}*]->(c)
            DETACH DELETE child, c, p
            RETURN count(p) as deleted
        """
        result = await self.db.query(query, {"post_id": post_id, "current_user_id": current_user_id})
        return result[0]["deleted"] > 0


    async def toggle_like(self, post_id: str, user_id: str) -> bool:
        return await self.toggle_relation(user_id, post_id, R.LIKED, N.USER, N.POST)
    