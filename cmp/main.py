from .neo4j import Neo4jConnection
from .postgres import PostgresConnection

if __name__ == "__main__":
	conn_neo4j = Neo4jConnection(uri="bolt://neo4j:7687", user="neo4j", password="password")
	conn_postgres = PostgresConnection(host="postgres", user="postgres", password="password", port=5432)
    
    conn_neo4j.query("CREATE (u:User {name: 'Ivan', email: 'ivan@mail.ru', city: 'Moscow'})")
