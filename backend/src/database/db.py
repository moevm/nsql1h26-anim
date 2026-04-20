from neo4j import AsyncGraphDatabase
from core.config import settings

class Neo4jDatabase:
  def __init__(self):
    self.driver = AsyncGraphDatabase.driver(
      settings.neo4j_uri,
      auth=(settings.neo4j_user, settings.neo4j_password)
    )
  
  async def close(self):
    await self.driver.close()
  
  async def init_db(self):
    queries = [
      "CREATE CONSTRAINT user_email_unique IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE",
      "CREATE CONSTRAINT user_username_unique IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE",
      "CREATE INDEX user_id_index IF NOT EXISTS FOR (u:User) ON (u.id)"
    ]
        
    for q in queries:
      await self.query(q)

  async def query(self, query: str, **params):
    async with self.driver.session() as session:
      result = await session.run(query, parameters=params)
      return [record.data() async for record in result]
    
db = Neo4jDatabase()