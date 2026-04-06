from neo4j import GraphDatabase
from seed import *

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        self.driver.close()

    def query(self, query, **kwargs):
        with self.driver.session() as session:
            result = session.run(query, **kwargs)
            return [record.data() for record in result]

    def create_constraints(self):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT user_email_unique IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE")
            session.run("CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
            session.run("CREATE CONSTRAINT post_id_unique IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE")
            session.run("CREATE INDEX taxon_name_idx IF NOT EXISTS FOR (t:Taxon) ON (t.name)")
            session.run("CREATE INDEX animal_species_idx IF NOT EXISTS FOR (a:Animal) ON (a.species)")

    def seed(self, data):
        users,    q = seed_users_neo(data['user']);         self.query(q, users=users)
        taxons,   q = seed_taxons_neo(data['taxon']);       self.query(q, taxons=taxons)
        animals,  q = seed_animals_neo(data['animal']);     self.query(q, animals=animals)
        tags,     q = seed_tags_neo(data['tag']);           self.query(q, tags=tags)
        posts,    q = seed_posts_neo(data['post']);         self.query(q, posts=posts)
        comments, q = seed_comments_neo(data['comment']);   self.query(q, comments=comments)

        edges, q = seed_taxon_hierarchy_neo(data['taxon']);             self.query(q, edges=edges)
        edges, q = seed_animal_belonged_to_taxon_neo(data['animal']);   self.query(q, edges=edges)
        edges, q = seed_user_authored_post_neo(data['post']);           self.query(q, edges=edges)
        edges, q = seed_post_observed_animal_neo(data['post']);         self.query(q, edges=edges)
        edges, q = seed_post_tagged_neo(data['post_tag']);              self.query(q, edges=edges)
        edges, q = seed_post_likes_neo(data['post_like']);              self.query(q, edges=edges)
        edges, q = seed_user_authored_comment_neo(data['comment']);     self.query(q, edges=edges)
        edges, q = seed_comment_on_post_neo(data['comment']);           self.query(q, edges=edges)
        edges, q = seed_comment_replied_neo(data['comment']);           self.query(q, edges=edges)
        edges, q = seed_comment_liked_neo(data['comment_like']);        self.query(q, edges=edges)
        edges, q = seed_follows_neo(data['follower']);                  self.query(q, edges=edges)

    def get_user_by_email(self, email):
        query = "MATCH (u:User {email: $email}) RETURN u"
        result = self.query(query, email=email)
        return result[0] if result else None

    def get_feed(self, limit=20):
        query = "MATCH (p:Post) RETURN p ORDER BY p.created_at DESC LIMIT $limit"
        return self.query(query, limit=limit) # Изменено с execute_query

    def get_filtered_feed(self, animal_type, start_date, end_date):
        query = """
            MATCH (a:Animal {species: $species})<-[:OBSERVED]-(p:Post)
            WHERE p.created_at >= $start AND p.created_at <= $end
            RETURN p ORDER BY p.created_at DESC
        """
        return self.query(query, species=animal_type, start=start_date, end=end_date) # Изменено

    def get_post_details(self, post_id):
        query = """
            MATCH (p:Post {id: $id})
            OPTIONAL MATCH (p)<-[:ON]-(c:Comment)
            RETURN p, collect(c) as comments
        """
        return self.query(query, id=post_id)
    
    def get_recommendations(self, user_id):
        query = """
        MATCH (u:User {id: $id})-[:FOLLOWED]->(friend)-[:FOLLOWED]->(fof:User)
        WHERE u <> fof AND NOT (u)-[:FOLLOWED]->(fof)
        RETURN fof.username, count(friend) as score
        ORDER BY score DESC LIMIT 10
        """
        return self.query(query, id=user_id)

    def get_taxon_tree_posts(self, taxon_name):
        query = """
        MATCH (root:Taxon {name: $name})<-[:PARENT_OF*0..]-(child:Taxon)<-[:BELONGED_TO]-(a:Animal)<-[:OBSERVED]-(p:Post)
        RETURN p LIMIT 50
        """
        return self.query(query, name=taxon_name)
    
    def get_social_recs(self, user_id):
        # UC-19: Поиск через 2 прыжка по связям FOLLOWS
        query = """
            MATCH (me:User {id: $id})-[:FOLLOWED]->(friend)-[:FOLLOWED]->(fof:User)
            WHERE me <> fof AND NOT (me)-[:FOLLOWED]->(fof)
            RETURN fof.id, count(friend) as score
            ORDER BY score DESC
            LIMIT 10
        """
        return self.query(query, id=user_id)

    def get_posts_by_taxon_recursive(self, taxon_name):
        # UC-20: Поиск вниз по дереву PARENT на любую глубину (*0..)
        query = """
            MATCH (root:Taxon {name: $name})<-[:PARENT_OF*0..]-(child:Taxon)
            MATCH (child)<-[:BELONGED_TO]-(a:Animal)<-[:OBSERVED]-(p:Post)
            RETURN p
            ORDER BY p.created_at DESC
            LIMIT 20
        """
        return self.query(query, name=taxon_name)