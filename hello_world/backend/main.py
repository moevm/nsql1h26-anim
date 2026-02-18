from neo4j import GraphDatabase
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Neo4jExample:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def clear_data(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
    
    def write_data(self):
        with self.driver.session() as session:
            queries = [
                "CREATE (u:User {name: 'Ivan', email: 'ivan@mail.ru', city: 'Москва'})",
                "CREATE (u:User {name: 'Maria', email: 'maria@yandex.ru', city: 'Санкт-Петербург'})",
                "CREATE (u:User {name: 'Petr', email: 'petr192@mail.ru', city: 'Москва'})",
                "CREATE (u:User {name: 'Vladislav', email: 'vladislav07@mail.ru', city: 'Владивосток'})",

                "CREATE (a:Animal {id: 1, species: 'Лиса обыкновенная', latin: 'Vulpes vulpes', category: 'Млекопитающие', endangered: false})",
                "CREATE (a:Animal {id: 2, species: 'Белый аист', latin: 'Ciconia ciconia', category: 'Птицы', endangered: false})",
                "CREATE (a:Animal {id: 3, species: 'Амурский тигр', latin: 'Panthera tigris altaica', category: 'Млекопитающие', endangered: true})",
                "CREATE (a:Animal {id: 4, species: 'Бурый медведь', latin: 'Ursus arctos', category: 'Млекопитающие', endangered: false})",
                "CREATE (a:Animal {id: 5, species: 'Орлан-белохвост', latin: 'Haliaeetus albicilla', category: 'Птицы', endangered: false})"
            ]
            for query in queries:
                session.run(query)
    
    def read_users(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User) RETURN u.name AS name, u.email AS email, u.city AS city ORDER BY u.name"
            )
            records = list(result)
            logger.info("\n---- Users ----")
            for r in records:
                logger.info(f"{r['name']} | {r['email']} | {r['city']}")
            return records
    
    def read_animals(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:Animal) RETURN a.species AS species, a.category AS category, a.endangered AS endangered ORDER BY a.category"
            )
            records = list(result)
            logger.info("\n---- Animals ----")
            for r in records:
                logger.info(f"{r['species']} | {r['category']}")
            return records

def main():
    user = "neo4j"
    uri = os.getenv("NEO4J_URI")
    password = os.getenv("NEO4J_PASSWORD")

    db = Neo4jExample(uri, user, password)
    
    db.clear_data()
    db.write_data()
    db.read_users()
    db.read_animals()
    db.close()

if __name__ == "__main__":
    main()