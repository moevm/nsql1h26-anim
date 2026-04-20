from abc import ABC, abstractmethod
from neo4j import AsyncSession
from faker import Faker

class Seeder(ABC):
  fake: Faker = Faker()

  @abstractmethod
  async def run(self, session: AsyncSession) -> None:
    pass