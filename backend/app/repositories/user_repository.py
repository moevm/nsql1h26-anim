from .base import BaseRepository
from typing import Optional
from neo4j.graph import Node

class UserRepository(BaseRepository):
  # Пусть даже 1 элемент в коллекции для универсальности метода
  async def create(self, data: list[dict]) -> None:
    query = """
    UNWIND $users AS props
    CREATE (u: User)
    SET u = props
    """

    await self.session.run(query, users=data)
    
  async def get(self, id: str) -> Optional[Node]:
    query = """
    MATCH (u:User {id: $user_id})
    RETURN u
    """

    results = await self.session.run(query, user_id=id)
    record = await results.single();
    if record: 
      return record['u'] 
    return None
    
  async def get_all(self) -> list[Node]:
    query="""
    MATCH (u:User)
    RETURN u
    """

    results = await self.session.run(query)
    return [record['u'] async for record in results]
  
  async def update(self, id: str, data: dict) -> Optional[Node]:
    query="""
    MATCH (u:User {id: $user_id})
    SET u += $props
    RETURN u
    """

    result = await self.session.run(query, user_id=id, props=data)
    record = await result.single()
    if record:
      return record['u']
    return None
  
  async def delete(self, id: str) -> None:
    query="""
    MATCH (u:User {id: $user_id})
    DETACH DELETE u
    """

    await self.session.run(query, user_id=id)