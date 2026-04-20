from database.db import db
from database.models import Animal
from schemas.request import AnimalCreate
from core.utils import get_now_iso, generate_uid

async def create_animal(data: AnimalCreate, taxon_id: str) -> Animal:
  now = get_now_iso()
  animal_id = generate_uid()

  query = """
  MATCH (tx:Taxon {id: $taxon_id})
  CREATE (a:Animal {
    id: $id,
    name: $name,
    scientific_name: $scientific_name,
    created_at: $now,
    updated_at: $now
  })
  CREATE (a)-[:BELONGED_TO]->(tx)
  RETURN a
  """

  result = await db.query(
    query,
    id=animal_id,
    taxon_id=taxon_id,
    name=data.name,
    scientific_name=data.scientific_name,
    now=now
  )

  if not result:
    return None
  
  return Animal(**result[0]['a'])