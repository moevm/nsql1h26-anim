from database.db import db

async def merge_tags(tags: list[str]) -> None:
  if not tags:
    return
  
  query = """
  UNWIND $tags AS tag
  MERGE (t:Tag {name: tag})
  """

  await db.query(query, tags=tags)
