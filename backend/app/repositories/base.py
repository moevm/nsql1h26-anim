from neo4j import AsyncSession

class BaseRepository:
  def __init__ (self, session: AsyncSession):
    self.session = session