from uuid import uuid4
from neo4j import AsyncSession
from .seeder import Seeder
from .mock import TAGS, HABITATS, TAXON_RANKS, TAXON_NAMES, SPECIES, OBSERVATION_TYPES
from datetime import datetime, timezone
from random import choice, choices
from faker import Faker

class PostSeeder(Seeder):
  count: int = 20
  batch_size: int = 5
  async def run(self, session: AsyncSession) -> None:
    result = await session.run("MATCH (u: USER) RETURN u.id AS id")
    user_ids = [r['id'] async for r in result]

    posts = [
      {
        'id': str(uuid4()),
        'title': self.fake.sentence(),
        'content': self.fake.text(max_nb_chars=500),
        'image_url': self.fake.image_url(),
        'location': self.fake.city(),        
        'created_at': datetime.now(timezone.utc).isoformat(),
        'updated_at': datetime.now(timezone.utc).isoformat(),
        'author_id': choice(user_ids),
        'tags': choices(TAGS, k=3),
        'observation_type': 'animal',
        'species': choice(SPECIES),
        'habitat': choice(HABITATS),
        'taxon_name': choice(TAXON_NAMES),
        'taxon_rank': choice(TAXON_RANKS)
      }
      for _ in range(self.count)
    ]

    query = """
      UNWIND $posts AS p
      MATCH (u:USER {id: p.author_id})
      CREATE(post: Post {
        id: p.id,
        title: p.title,
        content: p.content,
        image_url: p.image_url,
        location: p.location,
        created_at: p.created_at,
        updated_at: p.updated_at
      })
      CREATE (u)-[:AUTHORED]->(post)
      WITH post, p
      UNWIND p.tags AS tag
      MERGE (t:TAG {name: tag})
      CREATE (post)-[:TAGGED]->(t)
    """,
    
