from .base import BaseRepository
from typing import Optional
from neo4j.graph import Node

class PostRepository(BaseRepository):
  async def create(self, data: list[dict]) -> None:
    # User - [:AUTHORED] -> Post
    query = """
    UNWIND $posts AS props
    MATCH (u:User {id: props.author_id})
    CREATE (p:Post {
      id: props.id,
      title: props.title,
      content: props.content,
      image_url: props.image_url,
      location: props.location,
      created_at: props.created_at,
      updated_at: props.updated_at
    })
    CREATE (u)-[:AUTHORED]->(p)
    """

    await self.session.run(query, posts=data)

    # Post -[:TAGGED]-> Tag
    query="""
    UNWIND $posts AS props
    MATCH (p:Post {id: props.id})
    UNWIND props.tags AS tag
    MERGE (t: Tag {name: tag})
    CREATE (p)-[:TAGGED]->(t)
    """

    await self.session.run(query, posts=data)

    query="""
    UNWIND $posts AS props
            MATCH (p:Post {id: props.id})
            FOREACH (_ IN CASE props.observation_type WHEN 'animal' THEN [1] ELSE [] END |
                CREATE (o:AnimalObservation {
                    id: props.observation_id,
                    species: props.species,
                    habitat: props.habitat,
                    taxon_name: props.taxon_name,
                    taxon_rank: props.taxon_rank
                })
                CREATE (p)-[:HAS_OBSERVATION]->(o)
            )
            FOREACH (_ IN CASE props.observation_type WHEN 'general' THEN [1] ELSE [] END |
                CREATE (o:GeneralObservation {id: props.observation_id})
                CREATE (p)-[:HAS_OBSERVATION]->(o)
    """
  async def get(self, id) -> Optional[Node]:
    query="""
    
    """
  async def get_all(self):

  async def update(self, data):

  async def delete(self, id):