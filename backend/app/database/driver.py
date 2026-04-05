import os
from typing import AsyncGenerator
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession
from dotenv import load_dotenv

load_dotenv()

class Neo4jDatabase:
  def __init__(self) -> None:
    self._uri = os.getenv("NEO4J_URI", "")
    self._user = os.getenv("NEO4J_USER", "neo4j")
    self._password = os.getenv("NEO4J_PASSWORD", "password")
    self._driver: AsyncDriver | None = None
  
  async def connect(self) -> None:
    self._driver = AsyncGraphDatabase.driver(
      self._uri,
      auth=(self._user, self._password)
    )
    await self._driver.verify_connectivity()
  
  async def close(self) -> None:
    if self._driver:
      await self._driver.close()
      self._driver = None
  
  async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
    if not self._driver:
      raise RuntimeError("Neo4j Driver is not initialized")
    async with self._driver.session() as session:
      yield session

db = Neo4jDatabase()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
  async for session in db.get_session():
    yield session