from neo4j import GraphDatabase
from seed import *

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        self.driver.close()

    def query(self, query, **kwargs):
        with self.driver.session() as session:
            session.run(query, kwargs)

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