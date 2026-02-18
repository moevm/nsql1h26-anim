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
                "CREATE (p:Person {name: 'Ivan', age: 30, city: 'Moscow'})",
                "CREATE (p:Person {name: 'Maria', age: 25, city: 'St. Petersburg'})",
                "CREATE (p:Person {name: 'Petr', age: 35, city: 'Moscow'})"
            ]
            for query in queries:
                session.run(query)
    
    def read_data(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Person) RETURN p.name AS name, p.age AS age, p.city AS city ORDER BY p.name"
            )
            records = list(result)
            for record in records:
                logger.info(f"{record['name']}, {record['age']}, {record['city']}")
            return records
    
    def read_moscow_only(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Person {city: 'Moscow'}) RETURN p.name AS name, p.age AS age"
            )
            records = list(result)
            for record in records:
                logger.info(f"{record['name']}, {record['age']}")
            return records


def main():
    uri = os.getenv("NEO4J_URI")
    user = "neo4j"
    password = os.getenv("NEO4J_PASSWORD")
    
    db = Neo4jExample(uri, user, password)
    
    try:
        db.clear_data()
        db.write_data()
        db.read_data()
        db.read_moscow_only()
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()