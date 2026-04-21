from schemas.base import PostType
from schemas.request import PostCreate
from core.utils import get_now_iso, generate_uid
from services import taxon_service, animal_service, tag_service
from database.db import db
from database.models import User, PostFull, Animal, Taxon

def _map_row_to_post_full(row: dict) -> PostFull:
  taxons = []
  for node in row.get("taxonomy_chain", []):
    if node and node.get("id"):
      taxons.append(Taxon(
        id=node["id"], 
        name=node["name"], 
        rank=node["rank"]
    ))
            
  return PostFull(
    **row["p"],
    author=User(**row["u"]),
    animal=Animal(**row["a"]) if row.get("a") else None,
    taxonomy_chain=taxons,
    tags=row.get("tags", [])
  )

async def create_post(data: PostCreate, author_id: str) -> PostFull:
  try:
    now = get_now_iso()
    post_id = generate_uid()
    animal_id = None

    if data.type == PostType.animal and data.taxon and data.animal:
      taxon = await taxon_service.merge_taxon(data.taxon)
      animal = await animal_service.create_animal(data.animal, taxon.id)
      animal_id = animal.id
        
    await tag_service.merge_tags(data.tags)

    post_data = {
      "id": post_id,
      "title": data.title,
      "content": data.content,
      "image_url": data.image_url,
      "location": data.location,
      "type": data.type,
      "created_at": now,
      "updated_at": now
    }

    query = """
    MATCH (u:User {id: $author_id})
    CREATE (p:Post)
    SET p = $post_data
    CREATE (u)-[:AUTHORED]->(p)

    WITH p
    OPTIONAL MATCH (t:Tag) WHERE t.name IN $tags
    FOREACH (tag IN CASE WHEN t IS NOT NULL THEN [t] ELSE [] END |
      MERGE (p)-[:TAGGED]->(tag)
    )

    WITH p
    OPTIONAL MATCH (a:Animal {id: $animal_id})
    FOREACH (_ IN CASE WHEN a IS NOT NULL THEN [1] ELSE [] END |
      MERGE (p)-[:OBSERVED]->(a)
    )
        
    RETURN p.id AS id
    """

    result = await db.query(
      query,
      author_id=author_id,
      post_data=post_data,
      tags=data.tags,
      animal_id=animal_id
    )

    if not result:
      raise ValueError(f"User with id {author_id} not found. Register first!")

    return await get_by_id(post_id)
  except Exception as e:
    print(f"CRITICAL ERROR IN CREATE_POST: {e}")
    raise e
    
async def get_by_id(post_id: str) -> PostFull | None:
  query = """
  MATCH (u:User)-[:AUTHORED]->(p:Post {id: $post_id})
  OPTIONAL MATCH (p)-[:TAGGED]->(t:Tag)  
  OPTIONAL MATCH (p)-[:OBSERVED]->(a:Animal)
  OPTIONAL MATCH (a)-[:BELONGED_TO]->(leaf:Taxon)
  OPTIONAL MATCH (leaf)<-[:PARENT_OF*0..6]-(ancestor:Taxon)
  RETURN
    p, u,
    collect(DISTINCT t.name) AS tags,
    a,
    collect(DISTINCT ancestor) AS taxonomy_chain
  """

  result = await db.query(query, post_id=post_id)
  if not result or not result[0].get('p'):
    return None
  return _map_row_to_post_full(result[0])

async def get_all() -> list[PostFull]:
  query = """
  MATCH (u:User)-[:AUTHORED]->(p:Post)
  OPTIONAL MATCH (p)-[:TAGGED]->(t:Tag)
  OPTIONAL MATCH (p)-[:OBSERVED]->(a:Animal)
  OPTIONAL MATCH (a)-[:BELONGED_TO]->(leaf:Taxon)
  OPTIONAL MATCH (leaf)<-[:PARENT_OF*0..6]-(ancestor:Taxon)
    
  WITH p, u, a, 
    collect(DISTINCT t.name) AS tags,
    collect(DISTINCT ancestor) AS taxons
    
  RETURN 
    p, u, a, tags,
    [n IN taxons | {id: n.id, name: n.name, rank: n.rank}] AS taxonomy_chain
    ORDER BY p.created_at DESC
    """
    
  results = await db.query(query)
  return [_map_row_to_post_full(row) for row in results]

async def delete_post(post_id: str) -> bool:
  query = """
  MATCH (p:Post {id: $post_id})
  DETACH DELETE p
  RETURN count(p) as deleted_count
  """
        
  result = await db.query(query, post_id=post_id)
        
  if result and result[0].get("deleted_count", 0) > 0:
    return True
  return False