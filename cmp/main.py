import time
import random
from neo4j_db import Neo4jConnection
from postgres import PostgresConnection
from generate import generate_all

def run_benchmarks(pg, neo, data):
    print(f"\n{'Use Case / Query Description':<45} | {'Postgres (ms)':<15} | {'Neo4j (ms)':<15}")
    print("-" * 80)

    sample_user = random.choice(data['user'])
    sample_post = random.choice(data['post'])
    sample_animal = random.choice(data['animal'])
    sample_taxon = random.choice([t for t in data['taxon'] if t['rank'] != 'Species'])
    
    high_level_taxons = [t for t in data['taxon'] if t['rank'] in ['Kingdom', 'Phylum', 'Class']]
    sample_taxon = random.choice(high_level_taxons) if high_level_taxons else data['taxon'][0]
    
    test_cases = [
		("UC-01: Login (Find User by Email)", 
		lambda u=sample_user: pg.get_user_by_email(u['email']),
		lambda u=sample_user: neo.get_user_by_email(u['email'])),
				
		("UC-05: Filter Feed",
		lambda a=sample_animal: pg.get_filtered_feed(a['species'], "2026-01-01", "2026-12-31"),
		lambda a=sample_animal: neo.get_filtered_feed(a['species'], "2026-01-01", "2026-12-31")),
        
		("UC-06: Social Recommendations",
		lambda u=sample_user: pg.get_recommendations(u['id']),
		lambda u=sample_user: neo.get_recommendations(u['id'])),

		("UC-07: Deep Taxon Tree Search (Recursive)",
		lambda t=sample_taxon: pg.get_taxon_tree_posts(t['name']),
		lambda t=sample_taxon: neo.get_taxon_tree_posts(t['name'])),
				
		("UC-10: Post Detail",
		lambda p=sample_post: pg.get_post_details(p['id']),
		lambda p=sample_post: neo.get_post_details(p['id'])),

		("UC-19: Social Recommendations (FOF)",
		lambda u=sample_user: pg.get_social_recs(u['id']),
		lambda u=sample_user: neo.get_social_recs(u['id'])),

		("UC-20: Taxonomy Search (Recursive Tree)",
		lambda t=sample_taxon: pg.get_posts_by_taxon_recursive(t['name']),
		lambda t=sample_taxon: neo.get_posts_by_taxon_recursive(t['name'])),
	]

    for name, pg_func, neo_func in test_cases:
        for _ in range(3):
            pg_func()
            neo_func()
        t0 = time.perf_counter()
        pg_func()
        t_pg = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        neo_func()
        t_neo = (time.perf_counter() - t0) * 1000

        print(f"{name:<45} | {t_pg:>13.3f} | {t_neo:>13.3f}")

if __name__ == "__main__":
    conn_neo4j = Neo4jConnection(uri="bolt://neo4j:7687", user="neo4j", password="password")
    conn_postgres = PostgresConnection(host="postgres", user="postgres", password="password", port=5432)
    conn_neo4j.create_constraints()
    conn_postgres.create_table()
    conn_postgres.create_index()

    benchmarks_config = {
        "medium_load": {      
            "user": 1000, "taxon": 700, "tag": 200, "animal": 500,
            "post": 5000, "comment": 10000, "post_tag_max": 5,
            "post_like": 15000, "comment_like": 12000, "follower": 8000
        }
    }
    
    current_count = benchmarks_config["medium_load"]
    data = generate_all(current_count)
    
    conn_neo4j.seed(data)
    conn_postgres.seed(data)
    
    run_benchmarks(conn_postgres, conn_neo4j, data)