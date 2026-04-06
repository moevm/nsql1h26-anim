from neo4j_db import Neo4jConnection
from postgres import PostgresConnection
from generate import generate_all

if __name__ == "__main__":
	conn_neo4j = Neo4jConnection(uri="bolt://neo4j:7687", user="neo4j", password="password")
	conn_postgres = PostgresConnection(host="postgres", user="postgres", password="password", port=5432)
	conn_postgres.create_table()
	conn_postgres.create_index()

	benchmarks = {
    "test_drive": {      
        "user": 100,
        "taxon": 70,
        "tag": 50,
        "animal": 50,
        "post": 200,
        "comment": 300,
        "post_tag_max": 3,
        "post_like": 500,
        "comment_like": 400,
        "follower": 200
    },
    
    "medium_load": {     
        "user": 1000,
        "taxon": 700,
        "tag": 200,
        "animal": 500,
        "post": 5000,
        "comment": 10000,
        "post_tag_max": 5,
        "post_like": 15000,
        "comment_like": 12000,
        "follower": 8000
    },

    "heavy_stress": {   
        "user": 10000,
        "taxon": 2100,     
        "tag": 1000,
        "animal": 5000,
        "post": 50000,
        "comment": 150000,
        "post_tag_max": 10,
        "post_like": 250000,
        "comment_like": 200000,
        "follower": 150000
    }
	}
	current_count = benchmarks["medium_load"]
	data = generate_all(current_count)
	# conn_neo4j.seed(data)
	conn_postgres.seed(data)