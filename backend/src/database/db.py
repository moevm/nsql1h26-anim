from neo4j import AsyncGraphDatabase

from core.config import settings

class Neo4jDatabase:
    def __init__(self):
        self.driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password)
        )

    async def close(self):
        await self.driver.close()

    async def init_db(self):
        queries = [
            "CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT user_email_unique IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE",
            "CREATE CONSTRAINT user_username_unique IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE",

            "CREATE CONSTRAINT animal_id_unique IF NOT EXISTS FOR (a:Animal) REQUIRE a.id IS UNIQUE",
            "CREATE CONSTRAINT animal_sci_name_unique IF NOT EXISTS FOR (a:Animal) REQUIRE a.scientific_name IS UNIQUE",

            "CREATE INDEX animal_name_index IF NOT EXISTS FOR (a:Animal) ON (a.name)"
        ]

        for q in queries:
            await self.query(q)

    async def query(self, query: str, parameters: dict = None, **kwargs):
        all_params = {**(parameters or {}), **kwargs}
        async with self.driver.session() as session:
            result = await session.run(query, parameters=all_params)
            return [record.data() async for record in result]

    async def get_session(self):
        return self.driver.session()

db = Neo4jDatabase()